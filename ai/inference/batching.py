from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

import numpy as np


@dataclass(frozen=True)
class AudioChunk:
    index: int
    start: int
    end: int
    audio: np.ndarray


def iter_chunks(audio: np.ndarray, chunk_size: int, overlap: int = 0) -> Iterator[AudioChunk]:
    if chunk_size <= 0:
        yield AudioChunk(0, 0, audio.shape[-1], audio)
        return
    hop = max(1, chunk_size - max(0, overlap))
    total = audio.shape[-1]
    index = 0
    for start in range(0, total, hop):
        end = min(start + chunk_size, total)
        slicer = (..., slice(start, end))
        yield AudioChunk(index, start, end, audio[slicer])
        index += 1
        if end >= total:
            break


def overlap_add(chunks: list[AudioChunk], total_samples: int) -> np.ndarray:
    if not chunks:
        return np.array([], dtype=np.float32)
    first = chunks[0].audio
    output_shape = first.shape[:-1] + (total_samples,)
    output = np.zeros(output_shape, dtype=first.dtype)
    weight = np.zeros((total_samples,), dtype=np.float32)
    for chunk in chunks:
        length = chunk.end - chunk.start
        output[..., chunk.start:chunk.end] += chunk.audio[..., :length]
        weight[chunk.start:chunk.end] += 1
    weight[weight == 0] = 1
    return output / weight

