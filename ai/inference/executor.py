from __future__ import annotations

import time
from typing import Any

import numpy as np

from ai.models.base import AudioModel, safe_process
from ai.models.metadata import ModelResult


class InferenceExecutor:
    def run(
        self,
        model: AudioModel,
        audio: np.ndarray,
        sample_rate: int,
        config: dict[str, Any] | None = None,
    ) -> ModelResult:
        started = time.perf_counter()
        result = safe_process(model, audio, sample_rate, config)
        result.duration_ms = (time.perf_counter() - started) * 1000
        return result

