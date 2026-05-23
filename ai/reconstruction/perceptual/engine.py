from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from ai.runtime.audio_buffer import AudioBuffer


@dataclass(frozen=True)
class PerceptualReport:
    harshness_index: float
    listening_fatigue: float
    ambience_realism: float
    stereo_naturalness: float
    transient_realism: float
    spectral_balance: float

    @property
    def perceptual_score(self) -> float:
        penalties = (self.harshness_index, self.listening_fatigue)
        rewards = (self.ambience_realism, self.stereo_naturalness, self.transient_realism, self.spectral_balance)
        return float(np.clip((np.mean(rewards) + (1.0 - np.mean(penalties))) / 2.0, 0.0, 1.0))

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["perceptual_score"] = self.perceptual_score
        return payload


class PsychoacousticEngine:
    def analyze(self, audio: AudioBuffer) -> PerceptualReport:
        samples = audio.as_channels_first().samples.astype(np.float64, copy=False)
        mono = np.mean(samples, axis=0)
        spectrum = np.abs(np.fft.rfft(mono * np.hanning(mono.size))) + 1e-12 if mono.size else np.ones(1)
        freqs = np.fft.rfftfreq(mono.size, 1 / audio.sample_rate) if mono.size else np.zeros(1)
        total = float(np.sum(spectrum))
        harsh_band = float(np.sum(spectrum[(freqs >= 2500) & (freqs <= 6500)]) / total)
        high_band = float(np.sum(spectrum[freqs >= 10000]) / total)
        low_mid = float(np.sum(spectrum[(freqs >= 120) & (freqs <= 1200)]) / total)
        transients = np.abs(np.diff(mono, prepend=mono[:1])) if mono.size else np.zeros(1)
        transient_realism = float(np.clip(np.percentile(transients, 95) / (np.percentile(np.abs(mono), 95) + 1e-12), 0.0, 1.0))
        stereo = _stereo_naturalness(samples)
        ambience = float(np.clip(1.0 - np.std(_frame_rms(mono)) / (np.mean(_frame_rms(mono)) + 1e-12), 0.0, 1.0))
        balance = float(np.clip(1.0 - abs(low_mid - high_band * 3.0), 0.0, 1.0))
        harshness = float(np.clip(harsh_band * 5.0, 0.0, 1.0))
        fatigue = float(np.clip(harshness * 0.55 + max(0.0, high_band - 0.08) * 3.0, 0.0, 1.0))
        return PerceptualReport(harshness, fatigue, ambience, stereo, transient_realism, balance)


def _frame_rms(signal: np.ndarray, frame_size: int = 2048, hop_size: int = 1024) -> np.ndarray:
    if signal.size < frame_size:
        return np.array([float(np.sqrt(np.mean(signal**2))) if signal.size else 0.0])
    return np.array([float(np.sqrt(np.mean(signal[start : start + frame_size] ** 2))) for start in range(0, signal.size - frame_size + 1, hop_size)])


def _stereo_naturalness(samples: np.ndarray) -> float:
    if samples.shape[0] < 2:
        return 0.75
    left, right = samples[0], samples[1]
    denom = np.sqrt(np.sum(left**2) * np.sum(right**2))
    corr = float(np.sum(left * right) / denom) if denom > 0 else 1.0
    return float(np.clip(1.0 - abs(corr - 0.55) * 0.8, 0.0, 1.0))
