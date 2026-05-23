from __future__ import annotations

from typing import Protocol

from ai.adapters.base import RuntimeAdapterResult
from ai.runtime.audio_buffer import AudioBuffer
from ai.runtime.context import ExecutionContext


class DenoiseAdapter(Protocol):
    async def load(self, context: ExecutionContext) -> None:
        ...

    async def denoise(self, audio: AudioBuffer, context: ExecutionContext, options: dict | None = None) -> RuntimeAdapterResult:
        ...

