from __future__ import annotations

import numpy as np

from ai.reconstruction.core import ReconstructionContext, StageResult
from ai.runtime.audio_buffer import AudioBuffer


class PsychoacousticOptimizationStage:
    name = "psychoacoustic_optimization"

    def process(self, audio: AudioBuffer, context: ReconstructionContext) -> StageResult:
        samples = audio.as_channels_first().samples.astype(np.float32, copy=True)
        tilt = np.diff(samples, prepend=samples[..., :1], axis=-1) * 0.01
        optimized = samples + tilt
        peak = float(np.max(np.abs(optimized))) if optimized.size else 0.0
        if peak > 0.98:
            optimized *= 0.98 / peak
        return StageResult(self.name, AudioBuffer(samples=optimized, sample_rate=audio.sample_rate, layout="channels_first"), {"masking_aware": True, "fatigue_reduction": "conservative"})

