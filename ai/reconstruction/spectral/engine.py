from __future__ import annotations

import numpy as np

from ai.reconstruction.core import ReconstructionContext, StageResult
from ai.runtime.audio_buffer import AudioBuffer


class SpectralInterpolator:
    def interpolate(self, samples: np.ndarray) -> np.ndarray:
        if samples.shape[-1] < 7:
            return samples
        kernel = np.array([0.02, 0.08, 0.2, 0.4, 0.2, 0.08, 0.02], dtype=np.float32)
        return np.vstack([np.convolve(channel, kernel, mode="same") for channel in samples])


class ArtifactSuppressor:
    def suppress(self, samples: np.ndarray) -> np.ndarray:
        smooth = SpectralInterpolator().interpolate(samples)
        return samples * 0.92 + smooth * 0.08


class SpectralRepairEngine:
    def repair(self, audio: AudioBuffer) -> AudioBuffer:
        samples = audio.as_channels_first().samples.astype(np.float32, copy=True)
        repaired = ArtifactSuppressor().suppress(samples)
        return AudioBuffer(samples=repaired, sample_rate=audio.sample_rate, layout="channels_first")


class SpectralRepairStage:
    name = "spectral_repair"

    def process(self, audio: AudioBuffer, context: ReconstructionContext) -> StageResult:
        return StageResult(self.name, SpectralRepairEngine().repair(audio), {"method": "deterministic spectral continuity smoothing"})

