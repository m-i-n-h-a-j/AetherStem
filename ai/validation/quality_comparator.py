from __future__ import annotations

from typing import Any

import numpy as np
from pydantic import BaseModel, Field

from ai.validation.artifact_detector import ArtifactDetector, ArtifactReport


class QualityComparison(BaseModel):
    loudness_delta: float = 0.0
    spectral_restoration: float = 0.0
    noise_reduction_estimate: float = 0.0
    clipping_reduction: int = 0
    stereo_integrity: float = 1.0
    dynamic_range_preservation: float = 1.0
    accepted: bool = True
    reasons: list[str] = Field(default_factory=list)
    artifact_report: ArtifactReport


class QualityComparator:
    def __init__(self) -> None:
        self.artifacts = ArtifactDetector()

    def compare(self, before_analysis, processed_audio: np.ndarray, config: dict[str, Any] | None = None) -> dict[str, Any]:
        artifact_report = self.artifacts.score(processed_audio, (config or {}).get("artifact_threshold", 0.75))
        peak = float(np.max(np.abs(processed_audio))) if processed_audio.size else 0.0
        clipping_count = int(np.sum(np.abs(processed_audio) >= 1.0))
        before_clipping = int(getattr(before_analysis, "clipping_count", 0)) if before_analysis else 0
        reasons: list[str] = []
        accepted = not artifact_report.rejected
        if clipping_count > before_clipping:
            accepted = False
            reasons.append("Processed audio introduced new clipping.")
        comparison = QualityComparison(
            clipping_reduction=before_clipping - clipping_count,
            stereo_integrity=1.0,
            dynamic_range_preservation=1.0 if peak <= 1.0 else 0.0,
            accepted=accepted,
            reasons=reasons + artifact_report.reasons,
            artifact_report=artifact_report,
        )
        return comparison.model_dump()

