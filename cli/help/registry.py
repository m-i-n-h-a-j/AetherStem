from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CommandHelp:
    name: str
    category: str
    summary: str
    usage: str
    description: str
    options: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    related: list[str] = field(default_factory=list)
    troubleshooting: list[str] = field(default_factory=list)
    agent_notes: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return {
            "name": self.name,
            "category": self.category,
            "summary": self.summary,
            "usage": self.usage,
            "description": self.description,
            "options": self.options,
            "examples": self.examples,
            "related": self.related,
            "troubleshooting": self.troubleshooting,
            "agent_notes": self.agent_notes,
        }


class HelpRegistry:
    def __init__(self, commands: list[CommandHelp]) -> None:
        self._commands = {command.name: command for command in commands}
        self._aliases = {
            "runtime": "runtime-diagnostics",
            "models": "model-registry",
            "config": "config-info",
            "benchmark": "benchmark",
            "restore": "restore",
            "separate": "separate",
        }

    def all(self) -> list[CommandHelp]:
        return [self._commands[name] for name in sorted(self._commands)]

    def get(self, topic: str) -> CommandHelp | None:
        return self._commands.get(topic) or self._commands.get(self._aliases.get(topic, ""))

    def search(self, query: str) -> list[CommandHelp]:
        query = query.lower()
        return [
            command for command in self.all()
            if query in command.name.lower()
            or query in command.summary.lower()
            or query in command.description.lower()
            or query in command.category.lower()
        ]


default_help_registry = HelpRegistry([
    CommandHelp(
        name="analyze",
        category="analysis",
        summary="Run deterministic DSP analysis and write reports.",
        usage="aetherstem analyze INPUT [--output DIR] [--cache/--no-cache]",
        description="Inspects audio, runs loudness/spectrum/stereo/clipping/noise analysis, generates previews, and writes a JSON report.",
        examples=["aetherstem analyze song.flac", "aetherstem analyze song.wav --no-cache"],
        related=["inspect", "detect-lossy", "restore"],
    ),
    CommandHelp(
        name="separate",
        category="ai-runtime",
        summary="Separate audio into vocals, drums, bass, and other stems.",
        usage="aetherstem separate INPUT [--backend onnx] [--device cpu|cuda] [--chunk-size N] [--overlap RATIO] [--low-memory]",
        description="Runs the runtime separation graph through the Demucs-compatible adapter. Uses a configured ONNX model when available, otherwise executes the deterministic runtime fallback.",
        options=["--backend", "--device", "--chunk-size", "--overlap", "--low-memory", "--benchmark-runtime"],
        examples=["aetherstem separate song.flac --backend onnx --device cpu", "aetherstem separate song.wav --low-memory --benchmark-runtime"],
        related=["runtime-diagnostics", "benchmark", "config-info"],
        troubleshooting=["Run runtime-diagnostics if ONNX/CUDA is unavailable.", "Set ai.model_path or a registry manifest asset for real ONNX execution."],
        agent_notes=["Does not require orchestration changes when swapping compatible separation backends."],
    ),
    CommandHelp(
        name="restore",
        category="ai-runtime",
        summary="Run analysis-driven restoration.",
        usage="aetherstem restore INPUT [runtime options]",
        description="Runs DSP analysis, deterministic stage selection, runtime processing, validation, and export.",
        examples=["aetherstem restore damaged.flac", "aetherstem restore tape.wav --low-memory"],
        related=["preset", "denoise", "enhance"],
    ),
    CommandHelp(
        name="runtime-diagnostics",
        category="diagnostics",
        summary="Report runtime backends, providers, devices, profiles, and registry status.",
        usage="aetherstem runtime-diagnostics",
        description="Prints lightweight runtime diagnostics without loading model weights.",
        examples=["aetherstem runtime-diagnostics"],
        related=["help runtime", "troubleshoot"],
    ),
    CommandHelp(
        name="benchmark",
        category="benchmarking",
        summary="Measure workflow runtime and write benchmark reports.",
        usage="aetherstem benchmark INPUT [--output DIR]",
        description="Runs a restore workflow under the benchmark runner and records throughput, latency, backend, telemetry, profile, and chunk metrics when available.",
        examples=["aetherstem benchmark song.flac"],
        related=["separate", "runtime-diagnostics"],
    ),
    CommandHelp(
        name="model-registry",
        category="models",
        summary="List and resolve model manifests.",
        usage="aetherstem model-registry [--json]",
        description="Discovers local v0.5 model manifests and reports cache/compatibility metadata without loading weights.",
        examples=["aetherstem model-registry", "aetherstem model-registry --json"],
        related=["runtime-diagnostics", "config-info"],
    ),
    CommandHelp(
        name="config-info",
        category="configuration",
        summary="Inspect active configuration.",
        usage="aetherstem config-info [SECTION] [--json]",
        description="Shows current audio, pipeline, AI/runtime, path, and metadata config values.",
        examples=["aetherstem config-info ai", "aetherstem config-info --json"],
        related=["runtime-diagnostics", "help runtime"],
    ),
])

