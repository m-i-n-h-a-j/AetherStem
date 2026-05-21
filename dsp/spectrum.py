import numpy as np
import librosa
from models.audio_analysis import SpectrumAnalysis
from typing import Tuple

def analyze_spectrum(signal: np.ndarray, sample_rate: int) -> SpectrumAnalysis:
    """
    Performs spectral analysis on the audio signal.
    """
    # Use mono for most spectral features
    if len(signal.shape) == 2:
        mono_signal = librosa.to_mono(signal)
    else:
        mono_signal = signal

    # Spectral features
    centroid = librosa.feature.spectral_centroid(y=mono_signal, sr=sample_rate)
    rolloff = librosa.feature.spectral_rolloff(y=mono_signal, sr=sample_rate)
    bandwidth = librosa.feature.spectral_bandwidth(y=mono_signal, sr=sample_rate)
    
    # HF Cutoff Detection (approximate)
    # We can look for the frequency where energy drops significantly
    stft = np.abs(librosa.stft(mono_signal))
    avg_spectrum = np.mean(stft, axis=1)
    
    # Find HF cutoff: first bin from the top that has significant energy
    # Define significant as > -40dB relative to peak (more robust against artifacts)
    db_spectrum = librosa.amplitude_to_db(avg_spectrum)
    peak_db = np.max(db_spectrum)
    threshold = peak_db - 40
    
    freqs = librosa.fft_frequencies(sr=sample_rate)
    cutoff_idx = np.where(db_spectrum > threshold)[0]
    hf_cutoff = freqs[cutoff_idx[-1]] if len(cutoff_idx) > 0 else 0.0

    return SpectrumAnalysis(
        spectral_centroid_avg=float(np.mean(centroid)),
        spectral_rolloff_avg=float(np.mean(rolloff)),
        spectral_bandwidth_avg=float(np.mean(bandwidth)),
        hf_cutoff_hz=float(hf_cutoff),
        average_spectrum=avg_spectrum.tolist()[:1024]  # Limit size for model
    )
