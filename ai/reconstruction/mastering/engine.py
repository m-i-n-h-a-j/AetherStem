from __future__ import annotations

import numpy as np

from ai.reconstruction.core import MasteringProfile, ReconstructionContext, StageResult
from ai.runtime.audio_buffer import AudioBuffer


class MasteringStage:
    name = "mastering"

    def process(self, audio: AudioBuffer, context: ReconstructionContext) -> StageResult:
        samples = audio.as_channels_first().samples.astype(np.float32, copy=True)
        target_peak = 0.92 if context.mastering_profile == MasteringProfile.ARCHIVAL else 0.96
        peak = float(np.max(np.abs(samples))) if samples.size else 0.0
        if peak > target_peak:
            samples *= target_peak / peak
        return StageResult(self.name, AudioBuffer(samples=samples, sample_rate=audio.sample_rate, layout="channels_first"), {"profile": context.mastering_profile.value, "target_peak": target_peak})

