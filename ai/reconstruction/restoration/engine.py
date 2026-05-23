from __future__ import annotations

import numpy as np

from ai.reconstruction.core import ReconstructionContext, StageResult
from ai.runtime.audio_buffer import AudioBuffer


class DeclipStage:
    name = "declip"

    def process(self, audio: AudioBuffer, context: ReconstructionContext) -> StageResult:
        samples = audio.as_channels_first().samples.astype(np.float32, copy=True)
        clipped = np.abs(samples) >= 0.999
        samples = np.tanh(samples * 0.98)
        return StageResult(self.name, AudioBuffer(samples=samples, sample_rate=audio.sample_rate, layout="channels_first"), {"clipped_samples": int(np.sum(clipped))})


class DenoiseStage:
    name = "denoise"

    def process(self, audio: AudioBuffer, context: ReconstructionContext) -> StageResult:
        samples = audio.as_channels_first().samples.astype(np.float32, copy=True)
        if samples.shape[-1] >= 5:
            kernel = np.array([0.05, 0.15, 0.6, 0.15, 0.05], dtype=np.float32)
            smoothed = np.vstack([np.convolve(channel, kernel, mode="same") for channel in samples])
            samples = samples * 0.85 + smoothed * 0.15
        return StageResult(self.name, AudioBuffer(samples=samples, sample_rate=audio.sample_rate, layout="channels_first"), {"mode": "gentle deterministic smoothing"})


class DynamicRecoveryStage:
    name = "dynamic_recovery"

    def process(self, audio: AudioBuffer, context: ReconstructionContext) -> StageResult:
        samples = audio.as_channels_first().samples.astype(np.float32, copy=True)
        peak = float(np.max(np.abs(samples))) if samples.size else 0.0
        if peak > 0:
            expanded = np.sign(samples) * (np.abs(samples) ** 0.96)
            samples = expanded * min(0.98 / max(float(np.max(np.abs(expanded))), 1e-9), 1.0)
        return StageResult(self.name, AudioBuffer(samples=samples, sample_rate=audio.sample_rate, layout="channels_first"), {"input_peak": peak})

