from pathlib import Path
import numpy as np
from audio_io.audio_loader import load_audio
from typing import Tuple

class PreprocessStage:
    def execute(self, input_path: Path, target_sr: int = None) -> Tuple[np.ndarray, int]:
        signal, sr = load_audio(input_path, sr=target_sr)
        return signal, sr
