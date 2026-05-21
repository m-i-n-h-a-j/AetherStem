import numpy as np

def count_clipping(signal: np.ndarray, threshold: float = 0.999) -> int:
    """
    Counts the number of clipped samples in the signal.
    """
    clipped = np.abs(signal) >= threshold
    return int(np.sum(clipped))
