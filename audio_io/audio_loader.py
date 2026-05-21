import librosa
import numpy as np
from pathlib import Path
from typing import Tuple, Optional
from utils.logger import logger

def load_audio(
    file_path: Path,
    sr: Optional[int] = None,
    mono: bool = False
) -> Tuple[np.ndarray, int]:
    """
    Loads an audio file and returns the signal and sample rate.
    Converts to float32 normalized between -1.0 and 1.0.
    
    Args:
        file_path: Path to the audio file.
        sr: Target sample rate. If None, uses native sample rate.
        mono: If True, downmixes to mono.
        
    Returns:
        Tuple of (signal, sample_rate)
    """
    if not file_path.exists():
        logger.error(f"Audio file not found: {file_path}")
        raise FileNotFoundError(f"Audio file not found: {file_path}")

    try:
        logger.info(f"Loading audio file: {file_path}")
        # librosa.load returns (y, sr)
        # y is a numpy array (channels, samples) if mono=False and stereo file
        # or (samples,) if mono=True or mono file
        signal, sample_rate = librosa.load(file_path, sr=sr, mono=mono)
        
        # Ensure float32
        if signal.dtype != np.float32:
            signal = signal.astype(np.float32)
            
        logger.info(f"Loaded {file_path.name}: sr={sample_rate}, shape={signal.shape}")
        return signal, sample_rate
        
    except Exception as e:
        logger.error(f"Failed to load audio file {file_path}: {e}")
        raise RuntimeError(f"Failed to load audio file {file_path}: {e}")

def validate_stereo(signal: np.ndarray) -> bool:
    """Checks if the loaded signal is stereo (2 channels)."""
    return len(signal.shape) == 2 and signal.shape[0] == 2
