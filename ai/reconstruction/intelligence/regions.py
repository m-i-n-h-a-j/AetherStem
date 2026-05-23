from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

import numpy as np

from ai.runtime.audio_buffer import AudioBuffer


class RegionType(StrEnum):
    SILENCE = "silence"
    PERCUSSION = "percussion"
    BASS = "bass"
    VOCAL_OR_TONAL = "vocal_or_tonal"
    AMBIENCE = "ambience"


@dataclass(frozen=True)
class RegionMap:
    frame_duration_seconds: float
    regions: tuple[RegionType, ...]
    confidence: tuple[float, ...]

    def counts(self) -> dict[str, int]:
        return {region.value: self.regions.count(region) for region in RegionType}


class RegionClassifier:
    def __init__(self, frame_size: int = 2048, hop_size: int = 1024) -> None:
        self.frame_size = frame_size
        self.hop_size = hop_size

    def classify(self, audio: AudioBuffer) -> RegionMap:
        mono = np.mean(audio.as_channels_first().samples.astype(np.float64, copy=False), axis=0)
        regions: list[RegionType] = []
        confidence: list[float] = []
        for frame in _frames(mono, self.frame_size, self.hop_size):
            rms = float(np.sqrt(np.mean(frame**2)))
            spectrum = np.abs(np.fft.rfft(frame * np.hanning(frame.size))) + 1e-12
            freqs = np.fft.rfftfreq(frame.size, 1 / audio.sample_rate)
            centroid = float(np.sum(freqs * spectrum) / np.sum(spectrum))
            transient = float(np.percentile(np.abs(np.diff(frame, prepend=frame[:1])), 95))
            if rms < 1e-4:
                region = RegionType.SILENCE
            elif transient > rms * 0.8 and centroid > 1500:
                region = RegionType.PERCUSSION
            elif centroid < 220:
                region = RegionType.BASS
            elif rms < 0.01 and centroid > 1000:
                region = RegionType.AMBIENCE
            else:
                region = RegionType.VOCAL_OR_TONAL
            regions.append(region)
            confidence.append(float(np.clip(rms * 8.0 + transient * 4.0, 0.0, 1.0)))
        return RegionMap(self.hop_size / audio.sample_rate, tuple(regions), tuple(confidence))


def _frames(signal: np.ndarray, frame_size: int, hop_size: int) -> list[np.ndarray]:
    if signal.size < frame_size:
        frame = np.zeros(frame_size, dtype=signal.dtype)
        frame[: signal.size] = signal
        return [frame]
    return [signal[start : start + frame_size] for start in range(0, signal.size - frame_size + 1, hop_size)]
