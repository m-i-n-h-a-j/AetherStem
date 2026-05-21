import numpy as np
from models.audio_analysis import StereoAnalysis

def analyze_stereo(signal: np.ndarray) -> StereoAnalysis:
    """
    Analyzes stereo width, mid/side energy, and mono compatibility.
    Expected signal shape: (2, samples).
    """
    if len(signal.shape) != 2 or signal.shape[0] != 2:
        return StereoAnalysis(
            stereo_width=0.0,
            mid_energy=1.0,
            side_energy=0.0,
            phase_correlation=1.0,
            is_mono=True
        )

    left = signal[0]
    right = signal[1]

    # Mid/Side
    mid = 0.5 * (left + right)
    side = 0.5 * (left - right)

    mid_energy = np.sum(mid**2)
    side_energy = np.sum(side**2)
    total_energy = mid_energy + side_energy
    
    if total_energy > 0:
        side_ratio = side_energy / total_energy
    else:
        side_ratio = 0.0

    # Phase correlation: cos(theta) = (L . R) / (|L| |R|)
    norm_l = np.linalg.norm(left)
    norm_r = np.linalg.norm(right)
    
    if norm_l > 0 and norm_r > 0:
        correlation = np.dot(left, right) / (norm_l * norm_r)
    else:
        correlation = 1.0

    return StereoAnalysis(
        stereo_width=float(side_ratio * 2.0), # Heuristic: 0 is mono, 1 is wide
        mid_energy=float(mid_energy),
        side_energy=float(side_energy),
        phase_correlation=float(correlation),
        is_mono=side_energy < 1e-6
    )
