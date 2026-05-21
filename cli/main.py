import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional

from utils.config_loader import config
from utils.logger import logger
from audio_io.audio_inspector import inspect_audio, validate_input
from audio_io.audio_converter import convert_to_wav, check_ffmpeg
from pipeline.runner import PipelineRunner
from utils.cache import AnalysisCache

app = typer.Typer(help="AetherStem: Professional-grade audio analysis and DSP intelligence pipeline.")
console = Console()
cache = AnalysisCache()

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
        console.print("[red]Validation failed.[/red] Please ensure the file is stereo and in a supported format (WAV, FLAC, MP3, M4A).")
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
