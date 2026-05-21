import numpy as np
import pytest
from dsp.loudness import analyze_loudness

def test_analyze_loudness_silence():
    # 1 second of silence
    sr = 44100
    signal = np.zeros((2, sr), dtype=np.float32)
    result = analyze_loudness(signal, sr)
    
    # Integrated loudness of silence should be very low (usually -inf or clipped at some value)
    assert result.integrated_lufs < -60
    assert result.true_peak_db < -60

def test_analyze_loudness_sine():
    # 1 second of 440Hz sine wave at 0.5 amplitude
    sr = 44100
    t = np.linspace(0, 1, sr)
    sine = 0.5 * np.sin(2 * np.pi * 440 * t)
    signal = np.vstack([sine, sine]).astype(np.float32)
    
    result = analyze_loudness(signal, sr)
    
    # 0.5 amplitude is -6dB FS peak
    assert -10 < result.integrated_lufs < -3
    assert -7 < result.true_peak_db < -5
