from typing import Protocol, runtime_checkable
import numpy as np

@runtime_checkable
class AudioModel(Protocol):
    """
    Protocol for future AI model integration (e.g., Demucs, UVR).
    This ensures all model wrappers follow a consistent interface.
    """
    def load(self):
        """Loads the model into memory/GPU."""
        ...

    def process(self, audio: np.ndarray, sample_rate: int) -> np.ndarray:
        """
        Processes the input audio and returns the result.
        
        Args:
            audio: Input signal as a numpy array.
            sample_rate: Sample rate of the input audio.
            
        Returns:
            Processed audio signal.
        """
        ...
