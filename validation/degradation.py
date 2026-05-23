from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np
from scipy import signal


DegradationKind = Literal["lowpass", "clipping", "bitcrush", "stereo_collapse", "transient_smear"]


@dataclass(frozen=True)
class DegradationProfile:
    kind: DegradationKind
    amount: float


def apply_degradation(samples: np.ndarray, sample_rate: int, profile: DegradationProfile) -> np.ndarray:
    audio = np.asarray(samples, dtype=np.float32)
    amount = float(np.clip(profile.amount, 0.0, 1.0))
    if profile.kind == "lowpass":
        cutoff = max(1000.0, sample_rate * (0.08 + 0.32 * (1.0 - amount)))
        sos = signal.butter(6, cutoff, btype="lowpass", fs=sample_rate, output="sos")
        return signal.sosfiltfilt(sos, audio, axis=-1).astype(np.float32)
    if profile.kind == "clipping":
        threshold = max(0.05, 1.0 - amount * 0.85)
        return np.clip(audio, -threshold, threshold).astype(np.float32)
    if profile.kind == "bitcrush":
        bits = max(4, int(round(16 - amount * 12)))
        levels = float(2 ** (bits - 1))
        return (np.round(audio * levels) / levels).astype(np.float32)
    if profile.kind == "stereo_collapse":
        if audio.ndim != 2:
            return audio.copy()
        mono = np.mean(audio, axis=0, keepdims=True)
        return (audio * (1.0 - amount) + mono * amount).astype(np.float32)
    if profile.kind == "transient_smear":
        width = max(1, int(1 + amount * sample_rate * 0.01))
        kernel = np.ones(width, dtype=np.float32) / width
        return np.apply_along_axis(lambda row: np.convolve(row, kernel, mode="same"), -1, audio).astype(np.float32)
    raise ValueError(f"unknown degradation profile: {profile.kind}")
