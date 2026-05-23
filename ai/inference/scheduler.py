from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScheduleHint:
    chunk_size: int
    overlap: int
    estimated_memory_mb: float


class InferenceScheduler:
    def plan(self, total_samples: int, channels: int, chunk_size: int, overlap_ratio: float) -> ScheduleHint:
        overlap = int(chunk_size * overlap_ratio)
        bytes_per_chunk = max(1, chunk_size) * max(1, channels) * 4
        return ScheduleHint(
            chunk_size=chunk_size,
            overlap=overlap,
            estimated_memory_mb=bytes_per_chunk / (1024 * 1024),
        )

