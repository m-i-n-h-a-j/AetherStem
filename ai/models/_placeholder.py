from __future__ import annotations

import time
from typing import Any

import numpy as np

from ai.models.metadata import ModelMetadata, ModelResult, StemResult


class PassthroughModel:
    metadata: ModelMetadata
    name: str
    version: str

    def __init__(self) -> None:
        self.name = self.metadata.name
        self.version = self.metadata.version
        self.loaded = False

    def load(self) -> None:
        self.loaded = True

    def process(
        self,
        audio: np.ndarray,
        sample_rate: int,
        config: dict[str, Any] | None = None,
    ) -> ModelResult:
        started = time.perf_counter()
        return ModelResult(
            audio=np.array(audio, copy=True),
            sample_rate=sample_rate,
            model=self.metadata,
            backend=(config or {}).get("backend", "placeholder"),
            device=(config or {}).get("device", "cpu"),
            duration_ms=(time.perf_counter() - started) * 1000,
            warnings=["Placeholder adapter used; no neural processing was applied."],
        )


class StemPassthroughModel(PassthroughModel):
    stems = ("vocals", "drums", "bass", "other")

    def process(
        self,
        audio: np.ndarray,
        sample_rate: int,
        config: dict[str, Any] | None = None,
    ) -> ModelResult:
        started = time.perf_counter()
        requested = (config or {}).get("stems") or self.stems
        stems = {
            stem: StemResult(name=stem, audio=np.array(audio, copy=True), sample_rate=sample_rate)
            for stem in requested
        }
        return ModelResult(
            stems=stems,
            sample_rate=sample_rate,
            model=self.metadata,
            backend=(config or {}).get("backend", "placeholder"),
            device=(config or {}).get("device", "cpu"),
            duration_ms=(time.perf_counter() - started) * 1000,
            warnings=["Placeholder separation used; all stems contain the original signal."],
        )

