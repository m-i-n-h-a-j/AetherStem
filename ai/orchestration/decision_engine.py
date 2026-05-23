from __future__ import annotations

from pydantic import BaseModel, Field


class ProcessingDecision(BaseModel):
    stage: str
    enabled: bool
    observed: float | int | bool | None = None
    threshold: float | int | bool | None = None
    reason: str


class ProcessingPlan(BaseModel):
    decisions: list[ProcessingDecision] = Field(default_factory=list)
    stages: list[str] = Field(default_factory=list)

    def enabled(self, stage: str) -> bool:
        return stage in self.stages


class DecisionEngine:
    def __init__(self, thresholds: dict | None = None) -> None:
        self.thresholds = {
            "noise_floor_db": -55.0,
            "lossy_confidence": 0.65,
            "clipping_count": 0,
            **(thresholds or {}),
        }

    def plan(self, analysis, quality=None, force: list[str] | None = None) -> ProcessingPlan:
        force = force or []
        decisions = [
            ProcessingDecision(
                stage="separate",
                enabled="separate" in force,
                reason="Separation explicitly requested." if "separate" in force else "Separation not requested.",
            ),
            self._noise_decision(analysis, force),
            self._clip_decision(analysis, force),
            self._lossy_decision(quality, force),
            ProcessingDecision(stage="validate", enabled=True, reason="Validation always runs after processing."),
            ProcessingDecision(stage="export", enabled=True, reason="Exports are required for reproducibility."),
        ]
        stages = [decision.stage for decision in decisions if decision.enabled]
        return ProcessingPlan(decisions=decisions, stages=stages)

    def _noise_decision(self, analysis, force: list[str]) -> ProcessingDecision:
        observed = float(getattr(analysis, "noise_floor_db", -120.0)) if analysis else -120.0
        threshold = self.thresholds["noise_floor_db"]
        enabled = "denoise" in force or observed > threshold
        return ProcessingDecision(
            stage="denoise",
            enabled=enabled,
            observed=observed,
            threshold=threshold,
            reason="Noise floor exceeds threshold." if enabled else "Noise floor below threshold.",
        )

    def _clip_decision(self, analysis, force: list[str]) -> ProcessingDecision:
        observed = int(getattr(analysis, "clipping_count", 0)) if analysis else 0
        threshold = self.thresholds["clipping_count"]
        enabled = "declip" in force or observed > threshold
        return ProcessingDecision(
            stage="declip",
            enabled=enabled,
            observed=observed,
            threshold=threshold,
            reason="Clipping detected." if enabled else "No clipping detected.",
        )

    def _lossy_decision(self, quality, force: list[str]) -> ProcessingDecision:
        observed = float(getattr(quality, "confidence", 0.0)) if quality else 0.0
        threshold = self.thresholds["lossy_confidence"]
        is_transcoded = bool(getattr(quality, "is_transcoded", False)) if quality else False
        enabled = "enhance" in force or (is_transcoded and observed >= threshold)
        return ProcessingDecision(
            stage="enhance",
            enabled=enabled,
            observed=observed,
            threshold=threshold,
            reason="Lossy/transcode confidence exceeds threshold." if enabled else "Lossy recovery not justified.",
        )
