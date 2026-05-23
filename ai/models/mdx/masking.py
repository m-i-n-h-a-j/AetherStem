import numpy as np


def soft_mask(target_magnitude: np.ndarray, residual_magnitude: np.ndarray, power: float = 2.0) -> np.ndarray:
    target = np.maximum(target_magnitude, 0) ** power
    residual = np.maximum(residual_magnitude, 0) ** power
    denominator = target + residual
    return np.divide(target, denominator, out=np.zeros_like(target, dtype=np.float32), where=denominator > 0)

