from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from ai.reconstruction.analysis.forensic import ForensicAnalyzer
from ai.runtime.audio_buffer import AudioBuffer


@dataclass(frozen=True)
class ArtifactDetection:
    kind: str
    confidence: float
    severity: float
    temporal_region: tuple[float, float]
    spectral_region_hz: tuple[float, float]
    recommended_strategy: str
    recoverability: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ArtifactHeatmap:
    spectral_artifact_map: np.ndarray
    temporal_confidence_map: np.ndarray
    reconstruction_danger_map: np.ndarray
    stereo_instability_map: np.ndarray
    transient_degradation_map: np.ndarray

    def summary(self) -> dict[str, float]:
        return {
            "spectral_artifact_mean": float(np.mean(self.spectral_artifact_map)),
            "temporal_confidence_mean": float(np.mean(self.temporal_confidence_map)),
            "reconstruction_danger_mean": float(np.mean(self.reconstruction_danger_map)),
            "stereo_instability_mean": float(np.mean(self.stereo_instability_map)),
            "transient_degradation_mean": float(np.mean(self.transient_degradation_map)),
        }


class ArtifactIntelligenceEngine:
    def __init__(self, frame_size: int = 2048, hop_size: int = 1024) -> None:
        self.frame_size = frame_size
        self.hop_size = hop_size
        self.forensic = ForensicAnalyzer()

    def analyze(self, audio: AudioBuffer) -> tuple[list[ArtifactDetection], ArtifactHeatmap]:
        report = self.forensic.analyze(audio)
        samples = audio.as_channels_first().samples.astype(np.float64, copy=False)
        mono = np.mean(samples, axis=0)
        duration = audio.duration_seconds
        detections: list[ArtifactDetection] = []
        artifacts = report.artifacts
        if artifacts.spectral_cutoff_hz < audio.sample_rate * 0.45:
            detections.append(
                ArtifactDetection(
                    "lowpass_truncation",
                    confidence=float(np.clip(1.0 - artifacts.spectral_cutoff_hz / (audio.sample_rate * 0.45), 0.0, 1.0)),
                    severity=float(np.clip(1.0 - artifacts.spectral_cutoff_hz / max(audio.sample_rate * 0.45, 1.0), 0.0, 1.0)),
                    temporal_region=(0.0, duration),
                    spectral_region_hz=(artifacts.spectral_cutoff_hz, audio.sample_rate / 2),
                    recommended_strategy="bandwidth_extension",
                    recoverability=report.feasibility.score,
                )
            )
        if artifacts.codec_ringing > 0.25:
            detections.append(self._global_detection("codec_ringing", artifacts.codec_ringing, duration, "spectral_repair"))
        if artifacts.transient_smear > 0.25:
            detections.append(self._global_detection("transient_blur", artifacts.transient_smear, duration, "transient_recovery"))
        if artifacts.stereo_collapse > 0.25:
            detections.append(self._global_detection("stereo_collapse", artifacts.stereo_collapse, duration, "stereo_reconstruction"))
        if artifacts.clipping_detected:
            detections.append(self._global_detection("clipping", 1.0, duration, "declip"))
        return detections, self._heatmap(mono, samples, audio.sample_rate, detections)

    def _global_detection(self, kind: str, severity: float, duration: float, strategy: str) -> ArtifactDetection:
        value = float(np.clip(severity, 0.0, 1.0))
        return ArtifactDetection(kind, value, value, (0.0, duration), (0.0, 24000.0), strategy, float(1.0 - value * 0.35))

    def _heatmap(
        self,
        mono: np.ndarray,
        samples: np.ndarray,
        sample_rate: int,
        detections: list[ArtifactDetection],
    ) -> ArtifactHeatmap:
        frames = _frame_signal(mono, self.frame_size, self.hop_size)
        if not frames:
            zeros = np.zeros((1, 1), dtype=np.float32)
            return ArtifactHeatmap(zeros, np.ones(1, dtype=np.float32), zeros, zeros.copy(), zeros.copy())
        window = np.hanning(self.frame_size)
        spectrum = np.vstack([np.abs(np.fft.rfft(frame * window)) for frame in frames])
        spectrum = spectrum / (np.max(spectrum) + 1e-12)
        spectral_map = np.clip(1.0 - spectrum, 0.0, 1.0).astype(np.float32)
        energy = np.array([np.sqrt(np.mean(frame**2)) for frame in frames], dtype=np.float64)
        confidence = np.clip(energy / (np.max(energy) + 1e-12), 0.0, 1.0).astype(np.float32)
        danger = np.full(len(frames), max((item.severity for item in detections), default=0.0), dtype=np.float32)
        transient = np.array([np.percentile(np.abs(np.diff(frame, prepend=frame[:1])), 95) for frame in frames])
        transient = np.clip(1.0 - transient / (np.max(transient) + 1e-12), 0.0, 1.0).astype(np.float32)
        stereo = np.full(len(frames), _stereo_instability(samples), dtype=np.float32)
        return ArtifactHeatmap(spectral_map, confidence, danger, stereo, transient)


def _frame_signal(signal: np.ndarray, frame_size: int, hop_size: int) -> list[np.ndarray]:
    if signal.size == 0:
        return []
    if signal.size < frame_size:
        padded = np.zeros(frame_size, dtype=signal.dtype)
        padded[: signal.size] = signal
        return [padded]
    return [signal[start : start + frame_size] for start in range(0, signal.size - frame_size + 1, hop_size)]


def _stereo_instability(samples: np.ndarray) -> float:
    if samples.shape[0] < 2:
        return 0.0
    left, right = samples[0], samples[1]
    denom = np.sqrt(np.sum(left**2) * np.sum(right**2))
    corr = float(np.sum(left * right) / denom) if denom > 0 else 1.0
    return float(np.clip(abs(corr - 0.55), 0.0, 1.0))
