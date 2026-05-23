from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ModulePolicy:
    name: str
    minimum_confidence: float
    safe_min: float
    safe_max: float
    danger_sensitivity: float = 0.5


class ConfidenceGate:
    def clamp(self, policy: ModulePolicy, confidence: float, requested_aggressiveness: float, danger: float = 0.0) -> float:
        confidence = float(np.clip(confidence, 0.0, 1.0))
        requested = float(np.clip(requested_aggressiveness, 0.0, 1.0))
        danger = float(np.clip(danger, 0.0, 1.0))
        if confidence < policy.minimum_confidence:
            return 0.0
        confidence_scale = (confidence - policy.minimum_confidence) / max(1.0 - policy.minimum_confidence, 1e-12)
        danger_scale = 1.0 - danger * policy.danger_sensitivity
        allowed = policy.safe_min + (policy.safe_max - policy.safe_min) * confidence_scale * danger_scale
        return float(np.clip(min(requested, allowed), 0.0, policy.safe_max))

    def plan(self, policies: list[ModulePolicy], confidence: float, requested: float, danger: float = 0.0) -> dict[str, float]:
        return {policy.name: self.clamp(policy, confidence, requested, danger) for policy in policies}
