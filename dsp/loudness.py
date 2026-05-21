import numpy as np
import pyloudnorm as pyln
from models.audio_analysis import LoudnessAnalysis
from utils.logger import logger

def analyze_loudness(signal: np.ndarray, sample_rate: int) -> LoudnessAnalysis:
    """
    Analyzes loudness using EBU R128 standard.
    Input signal should be in shape (channels, samples).
    """
    # pyloudnorm expects (samples, channels)
    if len(signal.shape) == 2 and signal.shape[0] < signal.shape[1]:
        data = signal.T
    else:
        data = signal

    # Integrated Loudness
    meter = pyln.Meter(sample_rate)
    integrated_lufs = float(meter.integrated_loudness(data))

    # Momentary Loudness Max (using blockwise loudness from default meter with 0.4s block_size)
    if hasattr(meter, "blockwise_loudness") and len(meter.blockwise_loudness) > 0:
        momentary_max = float(np.max(meter.blockwise_loudness))
    else:
        momentary_max = integrated_lufs

    # Short-term Loudness Max (using blockwise loudness with 3.0s block_size)
    try:
        short_term_meter = pyln.Meter(sample_rate, block_size=3.0, overlap=0.0)
        short_term_meter.integrated_loudness(data)
        if len(short_term_meter.blockwise_loudness) > 0:
            short_term_max = float(np.max(short_term_meter.blockwise_loudness))
        else:
            short_term_max = integrated_lufs
    except Exception:
        short_term_max = integrated_lufs

    # Loudness Range (LRA)
    try:
        lra = float(meter.loudness_range(data))
    except (AttributeError, ValueError):
        lra = 0.0

    # True Peak estimation (4x oversampling as per ITU-R BS.1770-4)
    try:
        from scipy.signal import resample
        oversampling_factor = 4
        num_samples = data.shape[0] * oversampling_factor
        resampled_data = resample(data, num_samples)
        peak_val = np.max(np.abs(resampled_data))
    except Exception:
        peak_val = np.max(np.abs(data))
    
    true_peak_db = float(20 * np.log10(peak_val)) if peak_val > 0 else -120.0
    
    if true_peak_db > 0.0:
        logger.warning(f"Intersample peak warning: True Peak is {true_peak_db:.2f} dBTP, which exceeds 0 dBFS (clipping may occur).")
    
    return LoudnessAnalysis(
        integrated_lufs=integrated_lufs,
        short_term_max=short_term_max,
        momentary_max=momentary_max,
        lra=lra,
        true_peak_db=true_peak_db
    )
