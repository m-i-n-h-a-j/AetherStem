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
            "validation": "validation",
            "validate": "validation",
            "adaptive": "adaptive-intelligence",
            "v0.7": "adaptive-intelligence",
            "restore": "restore",
            "separate": "separate",
            "reconstruction": "reconstruct",
            "forensics": "forensic",
            "archival": "archival",
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
        description="Runs the separation-only runtime graph through the Demucs-compatible adapter, then validates and exports. It uses a configured ONNX model when available, otherwise executes the deterministic runtime fallback.",
        options=["--backend", "--device", "--chunk-size", "--overlap", "--low-memory", "--benchmark-runtime"],
        examples=[
            "aetherstem separate song.flac --backend onnx --device cuda --chunk-size 524288 --overlap 0.85",
            "aetherstem separate song.wav --backend onnx --device cpu",
        ],
        related=["runtime-diagnostics", "benchmark", "config-info"],
        troubleshooting=[
            "Run runtime-diagnostics if ONNX/CUDA is unavailable.",
            "Set ai.model_path or a registry manifest asset for real ONNX execution.",
            "The separate workflow does not auto-run denoise, declip, or enhance stages.",
        ],
        agent_notes=["Legacy demucs-placeholder configuration is upgraded to demucs-runtime for ONNX separation."],
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
        description="Prints lightweight runtime diagnostics, ONNX providers, device summaries, selected runtime profile, and manifest discovery status without loading model weights.",
        examples=["aetherstem runtime-diagnostics"],
        related=["help runtime", "troubleshoot"],
    ),
    CommandHelp(
        name="runtime-benchmark",
        category="benchmarking",
        summary="Compare ONNX CPU, CUDA, and TensorRT provider latency.",
        usage="aetherstem runtime-benchmark [--iterations N] [--output DIR]",
        description="Runs a deterministic synthetic ONNX workload across CPU, CUDA, and TensorRT providers when available, reporting provider initialization failures instead of silently falling back.",
        options=["--iterations", "--output"],
        examples=["aetherstem runtime-benchmark", "aetherstem runtime-benchmark --iterations 50"],
        related=["runtime-diagnostics", "model-registry"],
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
        name="validation",
        category="validation",
        summary="Run the platform validation framework and write regression reports.",
        usage="python -m validation.run_full_validation [--quick] [--strict-static] [--output-dir DIR]",
        description="Runs the validation laboratory entry point covering config validation, import graph validation, pytest, deterministic synthetic DSP checks, golden-reference comparisons, and report generation. Enterprise tiers are scaffolded for hardware, long-duration, fuzz, perceptual, backend, and streaming validation.",
        options=["--quick", "--strict-static", "--output-dir"],
        examples=["python -m validation.run_full_validation --quick", "python -m validation.run_full_validation --quick --strict-static"],
        related=["benchmark", "runtime-diagnostics", "config-info"],
        troubleshooting=["Install validation tooling with the validation extra documented in README.md.", "Validation reports are written under reports/validation by default."],
        agent_notes=["This is a Python module entry point, not a Typer subcommand."],
    ),
    CommandHelp(
        name="adaptive-intelligence",
        category="architecture",
        summary="Explain the v0.7 adaptive artifact, stability, and hardware planning layer.",
        usage="aetherstem help adaptive-intelligence",
        description="Documents the v0.7 foundation for artifact intelligence, confidence-gated reconstruction, region classification, temporal and perceptual scoring, hardware-aware quality scaling, adaptive scheduling, memory planning, backend selection contracts, and deterministic graph fingerprints.",
        examples=["aetherstem help adaptive-intelligence"],
        related=["validation", "reconstruct", "runtime-diagnostics"],
        troubleshooting=["The v0.7 layer is an executable foundation; graph mutation and CLI commands are tracked in the OpenSpec task list."],
        agent_notes=["OpenSpec change: openspec/changes/aetherstem-core-v0-7-adaptive-intelligence/"],
    ),
    CommandHelp(
        name="model-registry",
        category="models",
        summary="List and resolve model manifests.",
        usage="aetherstem model-registry [--json]",
        description="Discovers local model manifests and reports task, backend compatibility, precision metadata, and cache status without loading weights.",
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
    CommandHelp(
        name="forensic",
        category="reconstruction",
        summary="Generate deterministic forensic source and artifact reports.",
        usage="aetherstem forensic INPUT [--output DIR]",
        description="Analyzes likely source type, codec artifacts, spectral ceiling, transient smear, stereo collapse, clipping, feasibility, confidence, and uncertainty.",
        examples=["aetherstem forensic song.mp3"],
        related=["reconstruct", "archival"],
        agent_notes=["Does not claim true lossless recovery from lossy sources."],
    ),
    CommandHelp(
        name="reconstruct",
        category="reconstruction",
        summary="Run offline high-quality reconstruction and remastering.",
        usage="aetherstem reconstruct INPUT --profile extreme --target-rate 192000 --multi-pass",
        description="Runs forensic analysis, adaptive reconstruction graph generation, reconstruction stages, evaluation, and float-safe high-resolution rendering.",
        options=["--profile", "--target-rate", "--output-format", "--multi-pass", "--harmonic-reconstruction", "--bandwidth-extension"],
        examples=["aetherstem reconstruct song.mp3 --profile extreme --target-rate 192000 --multi-pass --bandwidth-extension"],
        related=["forensic", "remaster", "archival", "upscale"],
        troubleshooting=["Use forensic first to inspect feasibility and uncertainty."],
    ),
    CommandHelp(
        name="remaster",
        category="reconstruction",
        summary="Run reconstruction-oriented remastering.",
        usage="aetherstem remaster INPUT [--mastering-profile studio]",
        description="Applies reconstruction graph stages with mastering profile controls.",
        examples=["aetherstem remaster mix.flac --mastering-profile studio"],
        related=["reconstruct", "archival"],
    ),
    CommandHelp(
        name="archival",
        category="reconstruction",
        summary="Run conservative archival reconstruction and high-resolution rendering.",
        usage="aetherstem archival INPUT --target-rate 192000",
        description="Uses archival reconstruction and mastering profiles with multi-pass refinement.",
        examples=["aetherstem archival tape.wav --target-rate 192000"],
        related=["forensic", "reconstruct"],
    ),
    CommandHelp(
        name="upscale",
        category="reconstruction",
        summary="Run bandwidth-focused high-resolution reconstruction.",
        usage="aetherstem upscale INPUT --target-rate 192000",
        description="Focuses on bandwidth extension, harmonic reconstruction, spectral repair, and high-resolution rendering.",
        examples=["aetherstem upscale song.flac --target-rate 192000"],
        related=["reconstruct", "forensic"],
    ),
])
