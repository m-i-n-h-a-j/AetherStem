from __future__ import annotations

from dataclasses import dataclass

from ai.runtime.memory_manager import MemoryManager


@dataclass(frozen=True)
class AdaptiveMemoryPlan:
    estimated_chunk_mb: float
    batch_size: int
    spill_to_disk: bool
    low_memory: bool


class AdaptiveMemoryPlanner:
    def __init__(self, manager: MemoryManager | None = None) -> None:
        self.manager = manager or MemoryManager()

    def plan(self, channels: int, chunk_size: int, available_mb: float | None, low_memory: bool = False) -> AdaptiveMemoryPlan:
        estimated = self.manager.estimate_audio_mb(channels, chunk_size)
        batch = self.manager.safe_batch_size(estimated, available_mb, low_memory)
        spill = bool(available_mb is not None and estimated > available_mb * 0.8)
        return AdaptiveMemoryPlan(estimated, batch, spill, low_memory or batch == 1)
