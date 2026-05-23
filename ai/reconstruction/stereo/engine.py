from __future__ import annotations

import numpy as np

from ai.reconstruction.core import ReconstructionContext, StageResult
from ai.runtime.audio_buffer import AudioBuffer


class StereoReconstructionStage:
    name = "stereo_reconstruction"

    def process(self, audio: AudioBuffer, context: ReconstructionContext) -> StageResult:
        samples = audio.as_channels_first().samples.astype(np.float32, copy=True)
        if samples.shape[0] < 2:
            samples = np.vstack([samples[0], samples[0]])
        mid = (samples[0] + samples[1]) * 0.5
        side = (samples[0] - samples[1]) * 0.5
        side *= 1.08
        reconstructed = np.vstack([mid + side, mid - side]).astype(np.float32)
        peak = float(np.max(np.abs(reconstructed))) if reconstructed.size else 0.0
        if peak > 0.98:
            reconstructed *= 0.98 / peak
        return StageResult(self.name, AudioBuffer(samples=reconstructed, sample_rate=audio.sample_rate, layout="channels_first"), {"width_gain": 1.08, "mono_compatible": True})

