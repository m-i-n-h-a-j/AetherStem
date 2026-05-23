import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional

from ai.backends.registry import default_backend_registry
from ai.batch import BatchState, scan_audio_files
from ai.orchestration.decision_engine import DecisionEngine
from ai.orchestration.graph import AudioGraph
from ai.orchestration.presets import PresetLoader
from ai.runtime.device_manager import DeviceManager
from benchmarks.runner import BenchmarkRunner
from utils.config_loader import config
from utils.logger import logger
from audio_io.audio_inspector import inspect_audio, validate_input
from audio_io.audio_converter import convert_to_wav, check_ffmpeg
from pipeline.stages.preprocess import PreprocessStage
from pipeline.runner import PipelineRunner
from utils.cache import AnalysisCache

app = typer.Typer(help="AetherStem: Professional-grade audio analysis and DSP intelligence pipeline.")
console = Console()
cache = AnalysisCache()

def _ai_config(extra: dict | None = None) -> dict:
    base = {
        "backend": config.pipeline.backend,
        "device": config.pipeline.device,
        "chunk_size": config.pipeline.chunk_size,
        "overlap_ratio": config.pipeline.overlap_ratio,
        "overlap": config.pipeline.overlap_ratio,
        "provider": config.ai.provider,
        "precision": config.ai.precision,
        "low_memory": config.ai.low_memory,
        "model_path": config.ai.model_path,
        "fallback_to_cpu": config.pipeline.fallback_to_cpu,
        "denoise_strength": config.ai.denoise_strength,
        "enhancement_intensity": config.ai.enhancement_intensity,
        "models": config.ai.models,
    }
    if extra:
        base.update(extra)
    return base

def _run_ai_workflow(
    workflow: str,
    input_path: Path,
    force: list[str] | None = None,
    output_dir: Optional[Path] = None,
    thresholds: dict | None = None,
    workflow_config: dict | None = None,
    runtime_overrides: dict | None = None,
    benchmark_runtime: bool = False,
):
    if not input_path.exists():
        console.print(f"[red]Error:[/red] File not found: {input_path}")
        raise typer.Exit(code=1)

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task(description=f"Analyzing {input_path.name}...", total=None)
            analysis_result = PipelineRunner(output_dir=output_dir).run(input_path)
            if not analysis_result.success:
                raise RuntimeError(analysis_result.error or "Analysis failed")

            progress.update(task, description=f"Preparing {workflow} graph...")
            signal, sample_rate = PreprocessStage().execute(input_path)
            engine = DecisionEngine({**config.ai.validation_thresholds, **(thresholds or {})})
            graph = AudioGraph(decision_engine=engine, output_root=output_dir or Path(config.paths.exports_dir))
            graph_config = _ai_config({**(workflow_config or {}), **(runtime_overrides or {})})

            def on_progress(stage: str, status: str) -> None:
                progress.update(task, description=f"{workflow}: {stage} {status}")

            def execute_graph():
                return graph.execute(
                    signal,
                    sample_rate,
                    analysis_result.analysis,
                    analysis_result.quality,
                    workflow=workflow,
                    input_path=input_path,
                    force=force,
                    config=graph_config,
                    progress=on_progress,
                )

            if benchmark_runtime:
                report = BenchmarkRunner(Path(config.paths.benchmarks_dir)).run(input_path, execute_graph)
                result = report["result"]
                result["runtime_benchmark"] = report["report"]
            else:
                result = execute_graph()
        console.print(f"[bold green]{workflow.capitalize()} complete:[/bold green] {result['run_dir']}")
        console.print(f"Manifest: [cyan]{result['manifest']}[/cyan]")
        return result
    except Exception as e:
        console.print(f"[red]{workflow.capitalize()} failed:[/red] {e}")
        raise typer.Exit(code=1)

@app.command()
def version():
    """Displays the current application version."""
    typer.echo(f"AetherStem v{config.metadata['version']}")

@app.command()
def inspect(input_path: Path):
    """Displays audio file metadata using a Rich table."""
    if not input_path.exists():
        console.print(f"[red]Error:[/red] File not found: {input_path}")
        raise typer.Exit(code=1)

    try:
        metadata = inspect_audio(input_path)
        
        table = Table(title=f"Metadata for {input_path.name}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Format", metadata["format"])
        table.add_row("Codec", metadata["codec"])
        table.add_row("Sample Rate", f"{metadata['sample_rate']} Hz")
        table.add_row("Channels", str(metadata["channels"]))
        table.add_row("Bit Depth", f"{metadata['bit_depth']} bit")
        table.add_row("Duration", f"{metadata['duration']:.2f} seconds")
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]Error during inspection:[/red] {e}")
        raise typer.Exit(code=1)

@app.command()
def process(
    input_path: Path,
    output_path: Optional[Path] = typer.Option(None, "--output", "-o", help="Custom output path for the converted WAV file.")
):
    """Validates and converts an audio file to 96kHz, 32-bit float WAV."""
    if not input_path.exists():
        console.print(f"[red]Error:[/red] File not found: {input_path}")
        raise typer.Exit(code=1)

    if not validate_input(input_path):
        console.print("[red]Validation failed.[/red] Please ensure the file is stereo and in a supported format (WAV, FLAC, MP3, M4A, Opus).")
        raise typer.Exit(code=1)

    try:
        console.print(f"Converting [green]{input_path.name}[/green]...")
        result_path = convert_to_wav(
            input_path=input_path,
            output_path=output_path,
            sample_rate=config.audio.sample_rate,
            bit_depth=config.audio.bit_depth
        )
        console.print(f"Successfully converted to: [bold cyan]{result_path}[/bold cyan]")
    except Exception as e:
        console.print(f"[red]Error during processing:[/red] {e}")
        raise typer.Exit(code=1)

@app.command()
def analyze(
    input_path: Path,
    output_dir: Optional[Path] = typer.Option(None, "--output", "-o", help="Custom output directory for reports and visualizations."),
    use_cache: bool = typer.Option(True, "--cache/--no-cache", help="Enable/disable analysis cache.")
):
    """Performs full DSP analysis, lossy detection, and visualization."""
    if not input_path.exists():
        console.print(f"[red]Error:[/red] File not found: {input_path}")
        raise typer.Exit(code=1)

    try:
        if use_cache:
            cached_result = cache.get(input_path)
            if cached_result:
                _display_analysis_result(cached_result)
                return

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task(description=f"Analyzing {input_path.name}...", total=None)
            runner = PipelineRunner(output_dir=output_dir)
            result = runner.run(input_path)

        if result.success:
            if use_cache:
                cache.set(input_path, result)
            _display_analysis_result(result)
        else:
            console.print(f"[red]Analysis failed:[/red] {result.error}")
            
    except Exception as e:
        console.print(f"[red]Error during analysis:[/red] {e}")
        raise typer.Exit(code=1)

@app.command()
def detect_lossy(input_path: Path):
    """Quickly detects if an audio file is likely a lossy transcode."""
    analyze(input_path, use_cache=True)

@app.command()
def spectrogram(input_path: Path, output_dir: Optional[Path] = typer.Option(None, "--output-dir", "-d")):
    """Generates a spectrogram for the input file."""
    analyze(input_path, output_dir=output_dir)

@app.command()
def waveform(input_path: Path, output_dir: Optional[Path] = typer.Option(None, "--output-dir", "-d")):
    """Generates a waveform for the input file."""
    analyze(input_path, output_dir=output_dir)

@app.command()
def phase(input_path: Path):
    """Performs stereo and phase analysis."""
    analyze(input_path, use_cache=True)

@app.command()
def restore(
    input_path: Path,
    output_dir: Optional[Path] = typer.Option(None, "--output", "-o", help="Export directory."),
    backend: Optional[str] = typer.Option(None, "--backend", help="Runtime backend: auto, onnx, or torch."),
    device: Optional[str] = typer.Option(None, "--device", help="Runtime device: auto, cpu, or cuda."),
    chunk_size: Optional[int] = typer.Option(None, "--chunk-size", help="Runtime chunk size in samples."),
    overlap: Optional[float] = typer.Option(None, "--overlap", help="Chunk overlap ratio."),
    low_memory: bool = typer.Option(False, "--low-memory", help="Use sequential low-memory runtime scheduling."),
    benchmark_runtime: bool = typer.Option(False, "--benchmark-runtime", help="Write runtime benchmark report."),
):
    """Runs analysis-driven restoration and writes restored audio plus reports."""
    _run_ai_workflow("restore", input_path, output_dir=output_dir, runtime_overrides=_runtime_overrides(backend, device, chunk_size, overlap, low_memory), benchmark_runtime=benchmark_runtime)

@app.command()
def separate(
    input_path: Path,
    output_dir: Optional[Path] = typer.Option(None, "--output", "-o", help="Export directory."),
    backend: Optional[str] = typer.Option(None, "--backend", help="Runtime backend: auto, onnx, or torch."),
    device: Optional[str] = typer.Option(None, "--device", help="Runtime device: auto, cpu, or cuda."),
    chunk_size: Optional[int] = typer.Option(None, "--chunk-size", help="Runtime chunk size in samples."),
    overlap: Optional[float] = typer.Option(None, "--overlap", help="Chunk overlap ratio."),
    low_memory: bool = typer.Option(False, "--low-memory", help="Use sequential low-memory runtime scheduling."),
    benchmark_runtime: bool = typer.Option(False, "--benchmark-runtime", help="Write runtime benchmark report."),
):
    """Generates vocals, drums, bass, and other stems."""
    _run_ai_workflow("separate", input_path, force=["separate"], output_dir=output_dir, runtime_overrides=_runtime_overrides(backend, device, chunk_size, overlap, low_memory), benchmark_runtime=benchmark_runtime)

@app.command()
def denoise(
    input_path: Path,
    output_dir: Optional[Path] = typer.Option(None, "--output", "-o", help="Export directory."),
    backend: Optional[str] = typer.Option(None, "--backend", help="Runtime backend: auto, onnx, or torch."),
    device: Optional[str] = typer.Option(None, "--device", help="Runtime device: auto, cpu, or cuda."),
    chunk_size: Optional[int] = typer.Option(None, "--chunk-size", help="Runtime chunk size in samples."),
    overlap: Optional[float] = typer.Option(None, "--overlap", help="Chunk overlap ratio."),
    low_memory: bool = typer.Option(False, "--low-memory", help="Use sequential low-memory runtime scheduling."),
    benchmark_runtime: bool = typer.Option(False, "--benchmark-runtime", help="Write runtime benchmark report."),
):
    """Performs configurable broadband denoising with validation."""
    _run_ai_workflow("denoise", input_path, force=["denoise"], output_dir=output_dir, runtime_overrides=_runtime_overrides(backend, device, chunk_size, overlap, low_memory), benchmark_runtime=benchmark_runtime)

@app.command()
def enhance(
    input_path: Path,
    output_dir: Optional[Path] = typer.Option(None, "--output", "-o", help="Export directory."),
    backend: Optional[str] = typer.Option(None, "--backend", help="Runtime backend: auto, onnx, or torch."),
    device: Optional[str] = typer.Option(None, "--device", help="Runtime device: auto, cpu, or cuda."),
    chunk_size: Optional[int] = typer.Option(None, "--chunk-size", help="Runtime chunk size in samples."),
    overlap: Optional[float] = typer.Option(None, "--overlap", help="Chunk overlap ratio."),
    low_memory: bool = typer.Option(False, "--low-memory", help="Use sequential low-memory runtime scheduling."),
    benchmark_runtime: bool = typer.Option(False, "--benchmark-runtime", help="Write runtime benchmark report."),
):
    """Runs validation-aware enhancement when analysis warrants it."""
    _run_ai_workflow("enhance", input_path, force=["enhance"], output_dir=output_dir, runtime_overrides=_runtime_overrides(backend, device, chunk_size, overlap, low_memory), benchmark_runtime=benchmark_runtime)

@app.command("runtime-diagnostics")
def runtime_diagnostics():
    """Reports runtime backend, provider, device, and optional dependency status."""
    table = Table(title="Runtime Diagnostics")
    table.add_column("Component", style="cyan")
    table.add_column("Status", style="magenta")
    for name, diagnostics in default_backend_registry.diagnostics().items():
        table.add_row(f"backend:{name}", str(diagnostics))
    for device in DeviceManager().devices():
        table.add_row(f"device:{device.name}", str({"available": device.available, "memory_total_mb": device.memory_total_mb, "diagnostics": device.diagnostics or {}}))
    console.print(table)

@app.command("preset")
def run_preset(
    preset_name: str,
    input_path: Path,
    output_dir: Optional[Path] = typer.Option(None, "--output", "-o", help="Export directory."),
):
    """Runs a YAML-defined restoration workflow."""
    try:
        preset = PresetLoader().load(preset_name)
    except Exception as e:
        console.print(f"[red]Preset failed:[/red] {e}")
        raise typer.Exit(code=1)
    _run_ai_workflow(
        preset.workflow,
        input_path,
        force=preset.force,
        output_dir=output_dir,
        thresholds=preset.thresholds,
        workflow_config=preset.config,
    )

@app.command()
def batch(
    folder: Path,
    output_dir: Optional[Path] = typer.Option(None, "--output", "-o", help="Export directory."),
    force: bool = typer.Option(False, "--force", help="Reprocess files already marked complete."),
):
    """Recursively restores supported audio files with isolated per-file results."""
    if not folder.exists() or not folder.is_dir():
        console.print(f"[red]Error:[/red] Folder not found: {folder}")
        raise typer.Exit(code=1)
    export_root = output_dir or Path(config.paths.exports_dir)
    state = BatchState(export_root / "batch_state.json")
    files = state.pending(scan_audio_files(folder), force=force)
    console.print(f"Queued {len(files)} file(s).")
    for audio_file in files:
        try:
            _run_ai_workflow("restore", audio_file, output_dir=export_root)
            state.mark_completed(audio_file)
        except typer.Exit:
            state.mark_failed(audio_file, "Workflow failed")
    console.print(f"[bold green]Batch complete.[/bold green] State: {state.path}")

@app.command()
def benchmark(
    input_path: Path,
    output_dir: Optional[Path] = typer.Option(None, "--output", "-o", help="Benchmark report directory."),
):
    """Measures workflow runtime and writes a structured benchmark report."""
    runner = BenchmarkRunner(output_dir or Path(config.paths.benchmarks_dir))
    report = runner.run(input_path, lambda: _run_ai_workflow("restore", input_path))
    console.print(f"[bold green]Benchmark complete:[/bold green] {report['report']}")

def _runtime_overrides(
    backend: str | None,
    device: str | None,
    chunk_size: int | None,
    overlap: float | None,
    low_memory: bool,
) -> dict:
    values = {}
    if backend:
        values["backend"] = backend
    if device:
        values["device"] = device
    if chunk_size:
        values["chunk_size"] = chunk_size
    if overlap is not None:
        values["overlap"] = overlap
        values["overlap_ratio"] = overlap
    if low_memory:
        values["low_memory"] = True
    return values

def _display_analysis_result(result):
    """Helper to display PipelineResult in a rich format."""
    console.print(f"\n[bold green]Analysis Complete for {result.metadata.filename}[/bold green]\n")
    
    # Quality Table
    q_table = Table(title="Source Quality & Integrity")
    q_table.add_column("Metric", style="cyan")
    q_table.add_column("Value", style="magenta")
    
    if result.quality:
        color = "green" if not result.quality.is_transcoded else "yellow"
        q_table.add_row("Estimated Quality", f"[{color}]{result.quality.estimate.value}[/{color}]")
        q_table.add_row("Confidence", f"{result.quality.confidence:.2%}")
        q_table.add_row("HF Cutoff", f"{result.quality.detected_cutoff_hz/1000:.2f} kHz")
        q_table.add_row("Transcode Warning", "YES" if result.quality.is_transcoded else "NO")
    
    console.print(q_table)

    # Metrics Table
    if result.analysis:
        m_table = Table(title="DSP Metrics")
        m_table.add_column("Metric", style="cyan")
        m_table.add_column("Value", style="magenta")
        
        m_table.add_row("Integrated Loudness", f"{result.analysis.loudness.integrated_lufs:.2f} LUFS")
        m_table.add_row("True Peak", f"{result.analysis.loudness.true_peak_db:.2f} dBTP")
        m_table.add_row("Dynamic Range", f"DR{result.analysis.dynamic_range_dr:.1f}")
        m_table.add_row("Stereo Correlation", f"{result.analysis.stereo.phase_correlation:.2f}")
        m_table.add_row("Clipping Samples", str(result.analysis.clipping_count))
        m_table.add_row("Noise Floor", f"{result.analysis.noise_floor_db:.2f} dB")
        
        console.print(m_table)

    if result.artifacts:
        console.print("\n[bold cyan]Generated Artifacts:[/bold cyan]")
        for name, path in result.artifacts.items():
            console.print(f" - {name.capitalize()}: {path}")

if __name__ == "__main__":
    app()
