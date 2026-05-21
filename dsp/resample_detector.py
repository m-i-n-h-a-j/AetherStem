import numpy as np
from .spectrum import analyze_spectrum

def detect_resampling(signal: np.ndarray, sample_rate: int) -> bool:
    """
    Detects if a high-sample-rate file (e.g., 96kHz) is likely 
    upsampled from a lower native sample rate (e.g., 44.1kHz).
    """
    if sample_rate <= 44100:
        return False

    spec = analyze_spectrum(signal, sample_rate)
    cutoff = spec.hf_cutoff_hz
    
    # Common native sample rates / 2 (Nyquist)
    targets = [22050, 24000, 32000]
    
    for t in targets:
        # If cutoff is very close to a lower Nyquist frequency
        if abs(cutoff - t) < 500:
            return True
            
    return False
