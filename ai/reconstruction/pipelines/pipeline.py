from __future__ import annotations

from dataclasses import dataclass

from ai.reconstruction.analysis.forensic import ForensicAnalyzer
from ai.reconstruction.core import ReconstructionContext
from ai.reconstruction.evaluation.scoring import ReconstructionEvaluator
from ai.reconstruction.orchestration.builder import ReconstructionGraphBuilder
from ai.runtime.audio_buffer import AudioBuffer


@dataclass
class ReconstructionPipelineResult:
    source_report: dict
    stage_diagnostics: list[dict]
    evaluation: dict
    telemetry: dict
    profile: dict
    audio: AudioBuffer


class ReconstructionPipeline:
    def __init__(self) -> None:
        self.analyzer = ForensicAnalyzer()
        self.builder = ReconstructionGraphBuilder()
        self.evaluator = ReconstructionEvaluator()

    def run(self, audio: AudioBuffer, context: ReconstructionContext) -> ReconstructionPipelineResult:
        report = self.analyzer.analyze(audio)
        graph = self.builder.build(report, context.profile)
        reconstructed, diagnostics = graph.execute(audio, context)
        evaluation = self.evaluator.evaluate(audio, reconstructed, report)
        return ReconstructionPipelineResult(
            source_report=report.to_dict(),
            stage_diagnostics=diagnostics,
            evaluation=evaluation,
            telemetry=context.runtime.telemetry.model_dump(),
            profile={
                "reconstruction": context.profile.value,
                "mastering": context.mastering_profile.value,
                "target_rate": context.target_rate,
                "multi_pass": context.multi_pass,
                "philosophy": "plausible reconstruction, not true lossless recovery",
            },
            audio=reconstructed,
        )

