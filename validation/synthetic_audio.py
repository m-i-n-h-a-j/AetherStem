from __future__ import annotations

from dataclasses import dataclass
import hashlib

import numpy as np


@dataclass(frozen=True)
class SyntheticAudioFixture:
    name: str
    samples: np.ndarray
    sample_rate: int
    description: str
    checksum: str


def generate_synthetic_suite(sample_rate: int = 48000, duration_seconds: float = 1.0) -> list[SyntheticAudioFixture]:
    length = int(sample_rate * duration_seconds)
    time = np.arange(length, dtype=np.float64) / sample_rate
    rng = np.random.default_rng(1337)
    fixtures = {
        "sine_1khz": 0.5 * np.sin(2 * np.pi * 1000 * time),
        "impulse": _impulse(length),
        "white_noise": 0.1 * rng.standard_normal(length),
        "pink_noise": _pink_noise(length, rng) * 0.1,
        "log_sweep": _log_sweep(time, 40.0, sample_rate * 0.45),
        "transient_burst": _transient_burst(time),
        "stereo_phase": np.vstack([
            0.4 * np.sin(2 * np.pi * 440 * time),
            0.4 * np.sin(2 * np.pi * 440 * time + np.pi / 3),
        ]),
    }
    return [
        SyntheticAudioFixture(
            name=name,
            samples=np.asarray(samples, dtype=np.float32),
            sample_rate=sample_rate,
            description=_description(name),
            checksum=_checksum(np.asarray(samples, dtype=np.float32)),
        )
        for name, samples in fixtures.items()
    ]


def _impulse(length: int) -> np.ndarray:
    signal = np.zeros(length, dtype=np.float64)
    signal[length // 2] = 1.0
    return signal


def _pink_noise(length: int, rng: np.random.Generator) -> np.ndarray:
    white = rng.standard_normal(length)
    spectrum = np.fft.rfft(white)
    freqs = np.fft.rfftfreq(length)
    scale = np.ones_like(freqs)
    scale[1:] = 1.0 / np.sqrt(freqs[1:])
    pink = np.fft.irfft(spectrum * scale, n=length)
    return pink / max(float(np.max(np.abs(pink))), 1e-12)


def _log_sweep(time: np.ndarray, start_hz: float, end_hz: float) -> np.ndarray:
    duration = max(float(time[-1] - time[0]), 1e-12)
    k = np.log(end_hz / start_hz) / duration
    phase = 2 * np.pi * start_hz * (np.exp(k * time) - 1) / k
    return 0.35 * np.sin(phase)


def _transient_burst(time: np.ndarray) -> np.ndarray:
    carrier = np.sin(2 * np.pi * 3000 * time)
    envelope = np.exp(-((time - 0.5) ** 2) / 0.00008)
    return 0.8 * carrier * envelope


def _checksum(samples: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(samples).tobytes()).hexdigest()


def _description(name: str) -> str:
    return {
        "sine_1khz": "single-frequency tone for RMS, FFT, and aliasing checks",
        "impulse": "single-sample impulse for transient and phase checks",
        "white_noise": "deterministic broadband noise",
        "pink_noise": "deterministic 1/f noise",
        "log_sweep": "logarithmic sweep for spectral continuity checks",
        "transient_burst": "short high-frequency burst for temporal smearing checks",
        "stereo_phase": "stereo phase-offset tone for image stability checks",
    }[name]
