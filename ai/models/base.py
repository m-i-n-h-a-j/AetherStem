from __future__ import annotations

import time
from typing import Any, Protocol

import numpy as np

from ai.models.metadata import ModelMetadata, ModelResult


class ModelExecutionError(RuntimeError):
    """Raised when model inference fails after compatibility checks pass."""


class ModelUnavailableError(RuntimeError):
    """Raised when a requested adapter cannot load its optional runtime or weights."""


class ModelCompatibilityError(RuntimeError):
    """Raised when a model cannot run on the requested backend/device."""


class AudioModel(Protocol):
    name: str
    version: str
    metadata: ModelMetadata

    def load(self) -> None:
        ...

    def process(
        self,
        audio: np.ndarray,
        sample_rate: int,
        config: dict[str, Any] | None = None,
    ) -> ModelResult:
        ...


def safe_process(
    model: AudioModel,
    audio: np.ndarray,
    sample_rate: int,
    config: dict[str, Any] | None = None,
) -> ModelResult:
    started = time.perf_counter()
    try:
        model.load()
        result = model.process(audio, sample_rate, config or {})
        if result.duration_ms <= 0:
            result.duration_ms = (time.perf_counter() - started) * 1000
        return result
    except ModelUnavailableError:
        raise
    except Exception as exc:
        raise ModelExecutionError(f"{model.name} failed during inference: {exc}") from exc

