from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from ai.adapters.base import RuntimeAdapterResult
from ai.runtime.audio_buffer import AudioBuffer
from ai.runtime.context import ExecutionContext


@dataclass(frozen=True)
class SeparationOptions:
    stems: list[str] = field(default_factory=lambda: ["vocals", "drums", "bass", "other"])
    chunk_size: int = 44100 * 10
    overlap: float = 0.25
    model_path: str | None = None


class SeparationResult(RuntimeAdapterResult):
    pass


class SeparationAdapter(Protocol):
    async def load(self, context: ExecutionContext) -> None:
        ...

    async def separate(
        self,
        audio: AudioBuffer,
        context: ExecutionContext,
        options: SeparationOptions,
    ) -> SeparationResult:
        ...

