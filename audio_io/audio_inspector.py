import subprocess
import json
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from utils.logger import logger

def check_ffprobe() -> bool:
    """Checks if FFprobe is available in the system PATH."""
    return shutil.which("ffprobe") is not None

def inspect_audio(input_path: Path) -> Dict[str, Any]:
    """
    Extracts audio metadata using FFprobe.
    Returns a dictionary containing codec, sample rate, bit depth, channels, and duration.
    """
    if not check_ffprobe():
        logger.error("FFprobe not found in PATH. Please install FFmpeg (which includes FFprobe) to continue.")
        raise RuntimeError("FFprobe not found in PATH.")

    if not input_path.exists():
        logger.error(f"Input file not found: {input_path}")
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # FFprobe command:
    # -v error: show only errors
    # -select_streams a:0: select first audio stream
    # -show_entries stream=codec_name,sample_rate,channels,sample_fmt,duration,bits_per_raw_sample
    # -show_entries format=duration,format_name
    # -of json: output in JSON format
    
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "a:0",
        "-show_entries", "stream=codec_name,sample_rate,channels,sample_fmt,duration,bits_per_raw_sample",
        "-show_entries", "format=duration,format_name",
        "-of", "json",
        str(input_path)
    ]

    logger.info(f"Executing FFprobe command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        if not data.get("streams"):
            raise RuntimeError(f"No audio streams found in {input_path}")

        stream = data["streams"][0]
        format_info = data.get("format", {})

        # Extract relevant info
        metadata = {
            "filename": input_path.name,
            "format": format_info.get("format_name"),
            "codec": stream.get("codec_name"),
            "sample_rate": int(stream.get("sample_rate", 0)),
            "channels": int(stream.get("channels", 0)),
            "sample_fmt": stream.get("sample_fmt"),
            "duration": float(stream.get("duration") or format_info.get("duration") or 0),
            "bit_depth": _parse_bit_depth(stream)
        }
        
        logger.info(f"Metadata extracted for {input_path.name}")
        return metadata
    except subprocess.CalledProcessError as e:
        logger.error(f"FFprobe inspection failed: {e.stderr}")
        raise RuntimeError(f"FFprobe inspection failed: {e.stderr}")
    except Exception as e:
        logger.error(f"Error parsing FFprobe output: {e}")
        raise

def validate_input(input_path: Path) -> bool:
    """
    Validates that the input file is in a supported format and is stereo.
    Supported formats: WAV, FLAC, MP3, M4A.
    """
    supported_extensions = {".wav", ".flac", ".mp3", ".m4a"}
    if input_path.suffix.lower() not in supported_extensions:
        logger.error(f"Unsupported file extension: {input_path.suffix}. Supported: {supported_extensions}")
        return False

    try:
        metadata = inspect_audio(input_path)
        if metadata["channels"] != 2:
            logger.error(f"Input file is not stereo (channels: {metadata['channels']}). Only stereo files are supported.")
            return False
        
        logger.info(f"Input file validation successful: {input_path.name}")
        return True
    except Exception as e:
        logger.error(f"Validation failed due to error: {e}")
        return False

def _parse_bit_depth(stream: Dict[str, Any]) -> int:
    """Helper to parse bit depth from stream info."""
    # bits_per_raw_sample is often present for some codecs
    if "bits_per_raw_sample" in stream and stream["bits_per_raw_sample"].isdigit():
        return int(stream["bits_per_raw_sample"])
    
    # Otherwise infer from sample_fmt
    sample_fmt = stream.get("sample_fmt", "")
    if "flt" in sample_fmt or "32" in sample_fmt:
        return 32
    if "s16" in sample_fmt or "16" in sample_fmt:
        return 16
    if "s24" in sample_fmt or "24" in sample_fmt:
        return 24
    if "s64" in sample_fmt or "64" in sample_fmt:
        return 64
        
    return 0  # Unknown
