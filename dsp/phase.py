import numpy as np

def calculate_phase_correlation(signal: np.ndarray) -> float:
    """
    Calculates phase correlation between L and R channels.
    Range: -1.0 to 1.0. 
    1.0: mono/in-phase
    0.0: wide/uncorrelated
    -1.0: out-of-phase
    """
    if len(signal.shape) != 2 or signal.shape[0] != 2:
        return 1.0

    left = signal[0]
    right = signal[1]
    
    # Pearson correlation coefficient
    num = np.sum(left * right)
    den = np.sqrt(np.sum(left**2) * np.sum(right**2))
    
    if den > 0:
        return float(num / den)
    return 1.0

def detect_phase_flip(signal: np.ndarray) -> bool:
    """Detects if one channel is likely flipped in phase."""
    corr = calculate_phase_correlation(signal)
    return corr < -0.5
