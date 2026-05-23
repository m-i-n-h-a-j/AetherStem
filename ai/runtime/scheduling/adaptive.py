from __future__ import annotations

from dataclasses import dataclass

from ai.runtime.quality.scaling import QualityPlan


@dataclass(frozen=True)
class AdaptiveSchedulePlan:
    chunk_size: int
    overlap_ratio: float
    concurrency: int
    streaming: bool
    reason: str


class AdaptiveScheduler:
    def plan(self, quality: QualityPlan, sample_rate: int, recommended_concurrency: int, low_memory: bool = False) -> AdaptiveSchedulePlan:
        chunk_seconds = max(1.0, min(quality.temporal_context_seconds, 10.0))
        chunk_size = int(sample_rate * chunk_seconds)
        concurrency = 1 if low_memory or quality.hardware_tier == 0 else max(1, recommended_concurrency)
        streaming = low_memory or quality.hardware_tier <= 1
        reason = "low-memory streaming" if streaming else "quality-scaled batching"
        return AdaptiveSchedulePlan(chunk_size, quality.overlap_ratio, concurrency, streaming, reason)
