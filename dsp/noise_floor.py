import numpy as np
import librosa

def estimate_noise_floor(signal: np.ndarray) -> float:
    """
    Estimates the noise floor in dB.
    Uses the minimum energy window.
    """
    if len(signal.shape) == 2:
        mono = librosa.to_mono(signal)
    else:
        mono = signal

    # Calculate RMS in windows
    frame_length = 2048
    hop_length = 512
    rms = librosa.feature.rms(y=mono, frame_length=frame_length, hop_length=hop_length)[0]
    
    # Noise floor is the minimum RMS (approximate)
    min_rms = np.min(rms)
    if min_rms > 0:
        return float(librosa.amplitude_to_db(np.array([min_rms]))[0])
    return -120.0

def estimate_dynamic_range(signal: np.ndarray) -> float:
    """
    Estimates dynamic range (Crest factor or similar).
    """
    if len(signal.shape) == 2:
        mono = librosa.to_mono(signal)
    else:
        mono = signal

    peak = np.max(np.abs(mono))
    rms = np.sqrt(np.mean(mono**2))
    
    if rms > 0:
        crest_factor = peak / rms
        return float(20 * np.log10(crest_factor))
    return 0.0
