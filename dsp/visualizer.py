import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display
from pathlib import Path
from typing import Optional

def generate_spectrogram(
    signal: np.ndarray, 
    sample_rate: int, 
    output_path: Path,
    title: str = "Spectrogram"
) -> Path:
    """Generates and saves a spectrogram PNG."""
    plt.figure(figsize=(12, 8))
    
    if len(signal.shape) == 2:
        mono = librosa.to_mono(signal)
    else:
        mono = signal
        
    D = librosa.amplitude_to_db(np.abs(librosa.stft(mono)), ref=np.max)
    librosa.display.specshow(D, sr=sample_rate, x_axis='time', y_axis='hz')
    plt.colorbar(format='%+2.0f dB')
    plt.title(title)
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path

def generate_waveform(
    signal: np.ndarray, 
    sample_rate: int, 
    output_path: Path,
    title: str = "Waveform"
) -> Path:
    """Generates and saves a waveform PNG."""
    plt.figure(figsize=(12, 4))
    librosa.display.waveshow(signal, sr=sample_rate)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path

def generate_vectorscope(
    signal: np.ndarray,
    output_path: Path,
    title: str = "Stereo Vectorscope"
) -> Path:
    """Generates and saves a stereo vectorscope (L vs R) PNG."""
    if len(signal.shape) != 2 or signal.shape[0] != 2:
        return output_path # Cannot generate for mono

    left = signal[0]
    right = signal[1]
    
    # Downsample for performance
    step = max(1, len(left) // 5000)
    l_plot = left[::step]
    r_plot = right[::step]
    
    # Rotate 45 degrees for standard vectorscope view (Mid/Side axis)
    mid = (l_plot + r_plot) / np.sqrt(2)
    side = (l_plot - r_plot) / np.sqrt(2)

    plt.figure(figsize=(8, 8))
    plt.scatter(side, mid, s=1, alpha=0.1, c='cyan')
    plt.axhline(0, color='white', lw=0.5)
    plt.axvline(0, color='white', lw=0.5)
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title(title)
    plt.style.use('dark_background')
    
    plt.savefig(output_path)
    plt.close()
    return output_path

def generate_phase_correlation_graph(
    signal: np.ndarray,
    sample_rate: int,
    output_path: Path,
    title: str = "Phase Correlation Over Time"
) -> Path:
    """Generates and saves a phase correlation over time PNG."""
    if len(signal.shape) != 2 or signal.shape[0] != 2:
        return output_path # Cannot generate for mono
        
    left = signal[0]
    right = signal[1]
    
    # Calculate window-based correlation
    window_size = 4096
    hop_size = 1024
    num_samples = len(left)
    
    times = []
    correlations = []
    
    for start in range(0, num_samples - window_size, hop_size):
        end = start + window_size
        l_win = left[start:end]
        r_win = right[start:end]
        
        num = np.sum(l_win * r_win)
        den = np.sqrt(np.sum(l_win**2) * np.sum(r_win**2))
        
        corr = float(num / den) if den > 0 else 1.0
        correlations.append(corr)
        times.append((start + window_size / 2) / sample_rate)
        
    plt.figure(figsize=(12, 4))
    plt.plot(times, correlations, color='magenta', alpha=0.8)
    plt.axhline(0, color='gray', linestyle='--', linewidth=0.5)
    plt.axhline(1, color='green', linestyle=':', linewidth=0.5)
    plt.axhline(-1, color='red', linestyle=':', linewidth=0.5)
    plt.ylim(-1.1, 1.1)
    plt.xlabel("Time (seconds)")
    plt.ylabel("Phase Correlation")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    return output_path

