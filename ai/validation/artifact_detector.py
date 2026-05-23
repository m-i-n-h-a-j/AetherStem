from __future__ import annotations

import numpy as np
from pydantic import BaseModel, Field


class ArtifactReport(BaseModel):
    metallic_ringing: float = 0.0
    pre_echo: float = 0.0
    transient_smearing: float = 0.0
    hallucinated_harmonics: float = 0.0
    phase_corruption: float = 0.0
    stereo_instability: float = 0.0
    rejected: bool = False
    reasons: list[str] = Field(default_factory=list)


class ArtifactDetector:
    def score(self, audio: np.ndarray, threshold: float = 0.75) -> ArtifactReport:
        peak = float(np.max(np.abs(audio))) if audio.size else 0.0
        clipping_score = 1.0 if peak >= 1.0 else 0.0
        report = ArtifactReport(
            metallic_ringing=0.0,
            pre_echo=0.0,
            transient_smearing=0.0,
            hallucinated_harmonics=0.0,
            phase_corruption=0.0,
            stereo_instability=0.0,
        )
        if clipping_score >= threshold:
            report.rejected = True
            report.reasons.append("Processed audio peak reaches clipping threshold.")
        return report

