from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from ai.runtime.audio_buffer import AudioBuffer


@dataclass(frozen=True)
class TemporalStabilityReport:
    spectral_delta_continuity: float
    phase_continuity: float
    transient_trajectory_consistency: float
    ambience_persistence: float
    stereo_continuity: float

    @property
    def stability_score(self) -> float:
        values = (
            self.spectral_delta_continuity,
            self.phase_continuity,
            self.transient_trajectory_consistency,
            self.ambience_persistence,
            self.stereo_continuity,
        )
        return float(np.mean(values))

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["stability_score"] = self.stability_score
        return payload


class TemporalStabilityEngine:
    def __init__(self, frame_size: int = 2048, hop_size: int = 1024) -> None:
        self.frame_size = frame_size
        self.hop_size = hop_size

    def analyze(self, audio: AudioBuffer) -> TemporalStabilityReport:
        samples = audio.as_channels_first().samples.astype(np.float64, copy=False)
        mono = np.mean(samples, axis=0)
        frames = _frames(mono, self.frame_size, self.hop_size)
        spectra = np.vstack([np.abs(np.fft.rfft(frame * np.hanning(frame.size))) + 1e-12 for frame in frames])
        spectral_delta = _continuity(np.linalg.norm(np.diff(spectra, axis=0), axis=1), np.linalg.norm(spectra[:-1], axis=1))
        phase = np.unwrap(np.angle(np.fft.rfft(frames[0] * np.hanning(self.frame_size)))) if len(frames) == 1 else _phase_score(frames)
        transient = _continuity(np.abs(np.diff([np.percentile(np.abs(np.diff(frame, prepend=frame[:1])), 95) for frame in frames])), np.ones(max(len(frames) - 1, 1)))
        ambience = _ambience_persistence(frames)
        stereo = _stereo_continuity(samples, self.frame_size, self.hop_size)
        return TemporalStabilityReport(spectral_delta, float(np.mean(phase)) if np.ndim(phase) else float(phase), transient, ambience, stereo)


def _frames(signal: np.ndarray, frame_size: int, hop_size: int) -> list[np.ndarray]:
    if signal.size < frame_size:
        frame = np.zeros(frame_size, dtype=signal.dtype)
        frame[: signal.size] = signal
        return [frame]
    return [signal[start : start + frame_size] for start in range(0, signal.size - frame_size + 1, hop_size)]


def _continuity(delta: np.ndarray, reference: np.ndarray) -> float:
    if delta.size == 0:
        return 1.0
    ratio = float(np.mean(delta / (reference + 1e-12)))
    return float(1.0 / (1.0 + ratio))


def _phase_score(frames: list[np.ndarray]) -> float:
    phases = np.vstack([np.unwrap(np.angle(np.fft.rfft(frame * np.hanning(frame.size)))) for frame in frames])
    return _continuity(np.linalg.norm(np.diff(phases, axis=0), axis=1), np.ones(len(frames) - 1))


def _ambience_persistence(frames: list[np.ndarray]) -> float:
    tails = np.array([np.percentile(np.abs(frame), 20) for frame in frames])
    return _continuity(np.abs(np.diff(tails)), np.maximum(tails[:-1], 1e-12))


def _stereo_continuity(samples: np.ndarray, frame_size: int, hop_size: int) -> float:
    if samples.shape[0] < 2:
        return 1.0
    left_frames = _frames(samples[0], frame_size, hop_size)
    right_frames = _frames(samples[1], frame_size, hop_size)
    corrs = []
    for left, right in zip(left_frames, right_frames):
        denom = np.sqrt(np.sum(left**2) * np.sum(right**2))
        corrs.append(float(np.sum(left * right) / denom) if denom > 0 else 1.0)
    return _continuity(np.abs(np.diff(corrs)), np.ones(max(len(corrs) - 1, 1)))
