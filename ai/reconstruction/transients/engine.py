from __future__ import annotations

import numpy as np

from ai.reconstruction.core import ReconstructionContext, StageResult
from ai.runtime.audio_buffer import AudioBuffer


class TransientRecoveryStage:
    name = "transient_recovery"

    def process(self, audio: AudioBuffer, context: ReconstructionContext) -> StageResult:
        samples = audio.as_channels_first().samples.astype(np.float32, copy=True)
        attack = np.diff(samples, prepend=samples[..., :1], axis=-1)
        enhanced = samples + attack * 0.04
        peak = float(np.max(np.abs(enhanced))) if enhanced.size else 0.0
        if peak > 0.98:
            enhanced *= 0.98 / peak
        return StageResult(self.name, AudioBuffer(samples=enhanced, sample_rate=audio.sample_rate, layout="channels_first"), {"attack_amount": 0.04, "overshoot_prevented": peak > 0.98})

