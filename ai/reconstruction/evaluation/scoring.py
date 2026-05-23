from __future__ import annotations

import numpy as np

from ai.reconstruction.analysis.profiles import ForensicReport
from ai.runtime.audio_buffer import AudioBuffer


class ReconstructionEvaluator:
    def evaluate(self, before: AudioBuffer, after: AudioBuffer, report: ForensicReport) -> dict:
        source = before.as_channels_first().samples.astype(np.float64, copy=False)
        result = after.as_channels_first().samples.astype(np.float64, copy=False)
        length = min(source.shape[-1], result.shape[-1])
        source = source[..., :length]
        result = result[..., :length]
        clipping_after = int(np.sum(np.abs(result) >= 1.0))
        before_peak = float(np.max(np.abs(source))) if source.size else 0.0
        after_peak = float(np.max(np.abs(result))) if result.size else 0.0
        spectral_delta = _hf_ratio(result, after.sample_rate) - _hf_ratio(source, before.sample_rate)
        stereo_integrity = _stereo_integrity(result)
        transient_quality = float(np.clip(np.percentile(np.abs(np.diff(result, axis=-1)), 95) * 20.0, 0.0, 1.0)) if length > 1 else 0.0
        artifact_reduction = float(np.clip(0.5 + (before_peak - after_peak) * 0.2 + (1.0 if clipping_after == 0 else -0.2), 0.0, 1.0))
        return {
            "reconstruction_score": float(np.clip((artifact_reduction + stereo_integrity + transient_quality) / 3.0, 0.0, 1.0)),
            "artifact_reduction_score": artifact_reduction,
            "spectral_recovery_score": float(np.clip(0.5 + spectral_delta * 4.0, 0.0, 1.0)),
            "stereo_integrity_score": stereo_integrity,
            "transient_quality_score": transient_quality,
            "mastering_consistency_score": 1.0 if after_peak <= 0.98 else 0.5,
            "clipping_after": clipping_after,
            "restoration_potential": report.feasibility.potential,
            "confidence": report.confidence.confidence,
        }


def _hf_ratio(samples: np.ndarray, sample_rate: int) -> float:
    mono = np.mean(samples, axis=0)
    spectrum = np.abs(np.fft.rfft(mono)) + 1e-12
    freqs = np.fft.rfftfreq(mono.size, 1 / sample_rate)
    return float(np.sum(spectrum[freqs >= sample_rate * 0.35]) / np.sum(spectrum))


def _stereo_integrity(samples: np.ndarray) -> float:
    if samples.shape[0] < 2:
        return 0.75
    left, right = samples[0], samples[1]
    denom = np.sqrt(np.sum(left**2) * np.sum(right**2))
    corr = float(np.sum(left * right) / denom) if denom > 0 else 1.0
    return float(np.clip(1.0 - abs(corr - 0.55) * 0.5, 0.0, 1.0))

