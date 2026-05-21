import subprocess
import shutil
from pathlib import Path
from typing import Optional
from utils.logger import logger
from utils.config_loader import config

def check_ffmpeg() -> bool:
    """Checks if FFmpeg is available in the system PATH."""
    return shutil.which("ffmpeg") is not None

def convert_to_wav(
    input_path: Path,
    output_path: Optional[Path] = None,
    sample_rate: int = 96000,
    bit_depth: int = 32
) -> Path:
    """
    Converts an input audio file to a WAV file with specified sample rate and bit depth.
    Defaults to 96kHz, 32-bit float as per requirements.
    """
    if not check_ffmpeg():
        logger.error("FFmpeg not found in PATH. Please install FFmpeg to continue.")
        raise RuntimeError("FFmpeg not found in PATH.")

    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if output_path is None:
        temp_dir = Path(config.paths.temp_dir)
        temp_dir.mkdir(exist_ok=True)
        output_path = temp_dir / f"{input_path.stem}_converted.wav"

    # FFmpeg command:
    # -i: input file
    # -ar: sample rate
    # -ac: audio channels (enforce stereo if possible, or keep as is)
    # -sample_fmt: bit depth (f32 for 32-bit float)
    # -y: overwrite output
    
    # Map bit depth to ffmpeg codec and sample format
    if bit_depth == 32:
        codec = "pcm_f32le"
    else:
        codec = "pcm_s16le"
    
    cmd = [
        "ffmpeg",
        "-i", str(input_path),
        "-ar", str(sample_rate),
        "-ac", "2",  # Enforce stereo as per requirements
        "-c:a", codec,
        "-y",
        str(output_path)
    ]

    logger.info(f"Executing FFmpeg command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        logger.info(f"FFmpeg conversion successful. Output: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg conversion failed with return code {e.returncode}")
        logger.error(f"FFmpeg stderr: {e.stderr}")
        raise RuntimeError(f"FFmpeg conversion failed: {e.stderr}")
