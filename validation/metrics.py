from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np


EPSILON = 1e-12


@dataclass(frozen=True)
class AudioMetrics:
    sample_rate: int
    duration_seconds: float
    peak: float
    rms: float
    crest_factor: float
    dc_offset: float
    spectral_centroid_hz: float
    hf_energy_ratio: float
    phase_correlation: float
    temporal_stability: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compute_audio_metrics(samples: np.ndarray, sample_rate: int) -> AudioMetrics:
    audio = _channels_first(samples).astype(np.float64, copy=False)
    mono = np.mean(audio, axis=0)
    duration = mono.size / sample_rate if sample_rate > 0 else 0.0
    peak = float(np.max(np.abs(mono))) if mono.size else 0.0
    rms = float(np.sqrt(np.mean(mono**2))) if mono.size else 0.0
    crest = float(peak / max(rms, EPSILON))
    dc = float(np.mean(mono)) if mono.size else 0.0
    spectrum = np.abs(np.fft.rfft(mono)) if mono.size else np.array([0.0])
    freqs = np.fft.rfftfreq(mono.size, 1 / sample_rate) if mono.size else np.array([0.0])
    spectral_sum = float(np.sum(spectrum)) + EPSILON
    centroid = float(np.sum(freqs * spectrum) / spectral_sum)
    hf_mask = freqs >= sample_rate * 0.35
    hf_ratio = float(np.sum(spectrum[hf_mask]) / spectral_sum)
    return AudioMetrics(
        sample_rate=sample_rate,
        duration_seconds=float(duration),
        peak=peak,
        rms=rms,
        crest_factor=crest,
        dc_offset=dc,
        spectral_centroid_hz=centroid,
        hf_energy_ratio=hf_ratio,
        phase_correlation=_phase_correlation(audio),
        temporal_stability=_temporal_stability(mono),
    )


def compare_audio(
    reference: np.ndarray,
    candidate: np.ndarray,
    sample_rate: int,
    thresholds: dict[str, float] | None = None,
) -> dict[str, Any]:
    limits = {
        "waveform_rmse": 1e-4,
        "spectral_convergence": 1e-3,
        "log_spectral_distance": 0.05,
        "phase_correlation_delta": 0.02,
        "rms_delta_db": 0.05,
        **(thresholds or {}),
    }
    ref = _align(_channels_first(reference).astype(np.float64, copy=False))
    cand = _align(_channels_first(candidate).astype(np.float64, copy=False), ref.shape[-1])
    ref_mono = np.mean(ref, axis=0)
    cand_mono = np.mean(cand, axis=0)
    rmse = float(np.sqrt(np.mean((ref_mono - cand_mono) ** 2))) if ref_mono.size else 0.0
    ref_spec = np.abs(np.fft.rfft(ref_mono)) + EPSILON
    cand_spec = np.abs(np.fft.rfft(cand_mono)) + EPSILON
    convergence = float(np.linalg.norm(ref_spec - cand_spec) / (np.linalg.norm(ref_spec) + EPSILON))
    active_bins = ref_spec > (float(np.max(ref_spec)) * 1e-6)
    if not np.any(active_bins):
        active_bins = np.ones_like(ref_spec, dtype=bool)
    log_distance = float(
        np.sqrt(np.mean((20 * np.log10(ref_spec[active_bins]) - 20 * np.log10(cand_spec[active_bins])) ** 2))
    )
    ref_metrics = compute_audio_metrics(ref, sample_rate)
    cand_metrics = compute_audio_metrics(cand, sample_rate)
    phase_delta = abs(ref_metrics.phase_correlation - cand_metrics.phase_correlation)
    rms_delta_db = abs(_db(ref_metrics.rms) - _db(cand_metrics.rms))
    values = {
        "waveform_rmse": rmse,
        "spectral_convergence": convergence,
        "log_spectral_distance": log_distance,
        "phase_correlation_delta": phase_delta,
        "rms_delta_db": rms_delta_db,
    }
    failures = {name: value for name, value in values.items() if value > limits[name]}
    return {
        "passed": not failures,
        "metrics": values,
        "thresholds": limits,
        "failures": failures,
        "reference": ref_metrics.to_dict(),
        "candidate": cand_metrics.to_dict(),
    }


def _channels_first(samples: np.ndarray) -> np.ndarray:
    array = np.asarray(samples)
    if array.ndim == 1:
        return array.reshape(1, -1)
    if array.ndim != 2:
        raise ValueError("audio must be mono or 2D channel audio")
    return array if array.shape[0] <= array.shape[1] else array.T


def _align(samples: np.ndarray, length: int | None = None) -> np.ndarray:
    target = samples.shape[-1] if length is None else min(samples.shape[-1], length)
    return samples[..., :target]


def _phase_correlation(samples: np.ndarray) -> float:
    if samples.shape[0] < 2:
        return 1.0
    left, right = samples[0], samples[1]
    denom = np.sqrt(np.sum(left**2) * np.sum(right**2))
    return float(np.sum(left * right) / denom) if denom > EPSILON else 1.0


def _temporal_stability(mono: np.ndarray, frame_size: int = 1024, hop: int = 512) -> float:
    if mono.size < frame_size * 2:
        return 1.0
    spectra = []
    for start in range(0, mono.size - frame_size + 1, hop):
        frame = mono[start : start + frame_size] * np.hanning(frame_size)
        spectra.append(np.abs(np.fft.rfft(frame)) + EPSILON)
    if len(spectra) < 2:
        return 1.0
    stack = np.vstack(spectra)
    deltas = np.linalg.norm(np.diff(stack, axis=0), axis=1) / (np.linalg.norm(stack[:-1], axis=1) + EPSILON)
    return float(1.0 / (1.0 + np.mean(deltas)))


def _db(value: float) -> float:
    return float(20 * np.log10(max(value, EPSILON)))
