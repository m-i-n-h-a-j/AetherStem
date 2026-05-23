from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class QualityProfile(StrEnum):
    ULTRA_SAFE = "ultra_safe"
    BALANCED = "balanced"
    ENHANCED = "enhanced"
    STUDIO = "studio"
    FORENSIC_EXTREME = "forensic_extreme"


@dataclass(frozen=True)
class QualityPlan:
    profile: QualityProfile
    hardware_tier: int
    fft_size: int
    overlap_ratio: float
    temporal_context_seconds: float
    graph_complexity: int
    ai_passes: int
    psychoacoustic_depth: int
    stabilization_strength: float
    clamped: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class QualityScaler:
    _base = {
        QualityProfile.ULTRA_SAFE: (2048, 0.25, 1.0, 1, 0, 1, 0.9),
        QualityProfile.BALANCED: (4096, 0.5, 2.0, 2, 1, 2, 0.75),
        QualityProfile.ENHANCED: (8192, 0.625, 4.0, 3, 2, 3, 0.7),
        QualityProfile.STUDIO: (8192, 0.75, 6.0, 4, 2, 4, 0.65),
        QualityProfile.FORENSIC_EXTREME: (16384, 0.875, 10.0, 5, 3, 5, 0.6),
    }

    def plan(self, profile: QualityProfile | str, hardware_tier: int, available_memory_mb: float | None = None) -> QualityPlan:
        profile = QualityProfile(profile)
        requested = self._base[profile]
        max_complexity = max(1, hardware_tier + 1)
        memory_tier = 0 if available_memory_mb is not None and available_memory_mb < 2048 else hardware_tier
        effective_tier = min(hardware_tier, memory_tier)
        fft, overlap, context, complexity, passes, depth, stabilization = requested
        clamped = False
        if complexity > max_complexity:
            clamped = True
            scale = max_complexity / complexity
            fft = max(1024, int(fft * scale))
            overlap = min(overlap, 0.5 if effective_tier <= 1 else 0.75)
            context = max(0.5, context * scale)
            complexity = max_complexity
            passes = min(passes, max(0, effective_tier))
            depth = min(depth, max_complexity)
        return QualityPlan(profile, hardware_tier, int(fft), float(overlap), float(context), int(complexity), int(passes), int(depth), float(stabilization), clamped)
