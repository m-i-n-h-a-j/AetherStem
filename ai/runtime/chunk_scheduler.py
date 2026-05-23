from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ai.runtime.audio_buffer import AudioBuffer
from ai.runtime.memory_manager import MemoryManager


@dataclass(frozen=True)
class Chunk:
    index: int
    start: int
    end: int
    padded_end: int
    samples: np.ndarray


@dataclass(frozen=True)
class ChunkPlan:
    chunk_size: int
    overlap: int
    hop_size: int
    batch_size: int
    total_samples: int
    padded_samples: int
    estimated_memory_mb: float
    chunks: list[Chunk]


class ChunkScheduler:
    def __init__(self, memory_manager: MemoryManager | None = None) -> None:
        self.memory = memory_manager or MemoryManager()

    def plan(
        self,
        audio: AudioBuffer,
        chunk_size: int,
        overlap_ratio: float = 0.25,
        available_memory_mb: float | None = None,
        low_memory: bool = False,
    ) -> ChunkPlan:
        if chunk_size <= 0:
            chunk_size = audio.sample_count
        overlap = int(chunk_size * max(0.0, min(0.95, overlap_ratio)))
        hop = max(1, chunk_size - overlap)
        cf = audio.as_channels_first().samples
        total = audio.sample_count
        chunks: list[Chunk] = []
        for index, start in enumerate(range(0, total, hop)):
            end = min(start + chunk_size, total)
            padded_end = start + chunk_size
            chunk = cf[:, start:end]
            if chunk.shape[-1] < chunk_size:
                chunk = np.pad(chunk, ((0, 0), (0, chunk_size - chunk.shape[-1])))
            chunks.append(Chunk(index=index, start=start, end=end, padded_end=padded_end, samples=chunk))
            if end >= total:
                break
        estimated = self.memory.estimate_audio_mb(audio.channels or cf.shape[0], chunk_size)
        batch_size = self.memory.safe_batch_size(estimated, available_memory_mb, low_memory)
        return ChunkPlan(
            chunk_size=chunk_size,
            overlap=overlap,
            hop_size=hop,
            batch_size=batch_size,
            total_samples=total,
            padded_samples=chunks[-1].padded_end if chunks else 0,
            estimated_memory_mb=estimated,
            chunks=chunks,
        )


def overlap_add(chunks: list[tuple[Chunk, np.ndarray]], total_samples: int) -> np.ndarray:
    if not chunks:
        return np.zeros((0,), dtype=np.float32)
    first = chunks[0][1]
    output = np.zeros(first.shape[:-1] + (total_samples,), dtype=first.dtype)
    weights = np.zeros((total_samples,), dtype=np.float32)
    for chunk, values in chunks:
        end = min(chunk.end, total_samples)
        length = end - chunk.start
        output[..., chunk.start:end] += values[..., :length]
        weights[chunk.start:end] += 1
    weights[weights == 0] = 1
    return output / weights

