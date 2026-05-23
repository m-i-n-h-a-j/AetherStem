from __future__ import annotations

import numpy as np

from ai.reconstruction.core import ReconstructionContext, StageResult
from ai.runtime.audio_buffer import AudioBuffer


class HarmonicRegenerationStage:
    name = "harmonic_regeneration"

    def process(self, audio: AudioBuffer, context: ReconstructionContext) -> StageResult:
        samples = audio.as_channels_first().samples.astype(np.float32, copy=True)
        overtone = np.tanh(samples * 2.0) - samples
        regenerated = samples + overtone * 0.035
        regenerated = _headroom(regenerated)
        return StageResult(self.name, AudioBuffer(samples=regenerated, sample_rate=audio.sample_rate, layout="channels_first"), {"amount": 0.035, "phase_aware": True})


def _headroom(samples: np.ndarray) -> np.ndarray:
    peak = float(np.max(np.abs(samples))) if samples.size else 0.0
    return samples if peak <= 0.98 else samples * (0.98 / peak)

