import typer
from pathlib import Path
from rich.console import Console
from rich.table import Table
from typing import Optional

from utils.config_loader import config
from utils.logger import logger
from audio_io.audio_inspector import inspect_audio, validate_input
from audio_io.audio_converter import convert_to_wav, check_ffmpeg

app = typer.Typer(help="AetherStem: AI-assisted music source separation platform.")
console = Console()

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

if __name__ == "__main__":
    app()
