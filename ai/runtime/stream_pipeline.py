from __future__ import annotations

from collections.abc import Callable, Iterator

import numpy as np

from ai.runtime.audio_buffer import AudioBuffer
from ai.runtime.chunk_scheduler import Chunk, ChunkScheduler, overlap_add
from ai.runtime.context import ExecutionContext


class StreamPipeline:
    def __init__(self, scheduler: ChunkScheduler | None = None) -> None:
        self.scheduler = scheduler or ChunkScheduler()

    def chunks(self, audio: AudioBuffer, chunk_size: int, overlap_ratio: float, context: ExecutionContext) -> Iterator[Chunk]:
        plan = self.scheduler.plan(audio, chunk_size, overlap_ratio, low_memory=context.low_memory)
        for chunk in plan.chunks:
            context.cancellation.throw_if_cancelled()
            yield chunk

    def process(
        self,
        audio: AudioBuffer,
        chunk_size: int,
        overlap_ratio: float,
        context: ExecutionContext,
        fn: Callable[[np.ndarray], np.ndarray],
    ) -> np.ndarray:
        plan = self.scheduler.plan(audio, chunk_size, overlap_ratio, low_memory=context.low_memory)
        completed = []
        for chunk in plan.chunks:
            context.cancellation.throw_if_cancelled()
            completed.append((chunk, fn(chunk.samples)))
            context.progress.report("stream", len(completed), len(plan.chunks), "processed chunk")
        return overlap_add(completed, plan.total_samples)

