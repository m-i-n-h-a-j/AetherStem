from __future__ import annotations

import numpy as np

from ai.reconstruction.core import ReconstructionContext, StageResult
from ai.runtime.audio_buffer import AudioBuffer


class HighFrequencySynthesizer:
    def synthesize(self, samples: np.ndarray) -> np.ndarray:
        bright = np.diff(samples, prepend=samples[..., :1], axis=-1)
        return np.tanh(bright * 1.5) * 0.025


class SpectralRegenerator:
    def regenerate(self, samples: np.ndarray) -> np.ndarray:
        return samples + HighFrequencySynthesizer().synthesize(samples)


class BandwidthExtender:
    def extend(self, audio: AudioBuffer) -> AudioBuffer:
        samples = audio.as_channels_first().samples.astype(np.float32, copy=True)
        regenerated = SpectralRegenerator().regenerate(samples)
        peak = float(np.max(np.abs(regenerated))) if regenerated.size else 0.0
        if peak > 0.98:
            regenerated *= 0.98 / peak
        return AudioBuffer(samples=regenerated, sample_rate=audio.sample_rate, layout="channels_first")


class BandwidthExtensionStage:
    name = "bandwidth_extension"

    def process(self, audio: AudioBuffer, context: ReconstructionContext) -> StageResult:
        return StageResult(self.name, BandwidthExtender().extend(audio), {"method": "harmonic-aware deterministic HF synthesis"})

