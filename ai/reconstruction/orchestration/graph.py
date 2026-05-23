from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol

from ai.reconstruction.core import ReconstructionContext, StageResult
from ai.runtime.audio_buffer import AudioBuffer


class RestorationStage(Protocol):
    name: str

    def process(self, audio: AudioBuffer, context: ReconstructionContext) -> StageResult:
        ...


@dataclass
class ReconstructionGraph:
    stages: list[RestorationStage] = field(default_factory=list)

    def execute(self, audio: AudioBuffer, context: ReconstructionContext) -> tuple[AudioBuffer, list[dict]]:
        current = audio.astype("float32")
        diagnostics = []
        for stage in self.stages:
            context.runtime.cancellation.throw_if_cancelled()
            context.runtime.telemetry.emit("reconstruction_stage_started", stage=stage.name)
            with context.runtime.profiler.span(f"reconstruction:{stage.name}"):
                result = stage.process(current, context)
            current = result.audio
            context.runtime.telemetry.emit("reconstruction_stage_completed", stage=stage.name, diagnostics=result.diagnostics)
            diagnostics.append({"stage": stage.name, "diagnostics": result.diagnostics})
        return current, diagnostics

