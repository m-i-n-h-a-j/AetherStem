from __future__ import annotations

from dataclasses import dataclass

from ai.reconstruction.core import ReconstructionContext
from ai.reconstruction.pipelines.pipeline import ReconstructionPipeline, ReconstructionPipelineResult
from ai.runtime.audio_buffer import AudioBuffer


@dataclass(frozen=True)
class ReconstructionPass:
    index: int
    name: str


class MultiPassPipeline:
    def __init__(self, passes: list[ReconstructionPass] | None = None) -> None:
        self.passes = passes or [
            ReconstructionPass(1, "artifact_analysis"),
            ReconstructionPass(2, "restoration"),
            ReconstructionPass(3, "bandwidth_reconstruction"),
            ReconstructionPass(4, "mastering"),
            ReconstructionPass(5, "perceptual_optimization"),
        ]
        self.pipeline = ReconstructionPipeline()

    def run(self, audio: AudioBuffer, context: ReconstructionContext) -> ReconstructionPipelineResult:
        current = audio
        final = None
        pass_reports = []
        for reconstruction_pass in self.passes:
            context.runtime.telemetry.emit("reconstruction_pass_started", index=reconstruction_pass.index, name=reconstruction_pass.name)
            final = self.pipeline.run(current, context)
            current = final.audio
            pass_reports.append({"index": reconstruction_pass.index, "name": reconstruction_pass.name, "evaluation": final.evaluation})
            context.runtime.telemetry.emit("reconstruction_pass_completed", index=reconstruction_pass.index, name=reconstruction_pass.name)
        assert final is not None
        final.profile["passes"] = pass_reports
        final.telemetry = context.runtime.telemetry.model_dump()
        return final


class IterativeRefinement(MultiPassPipeline):
    pass

