import numpy as np
import pytest
from dsp.spectrum import analyze_spectrum

def test_analyze_spectrum_sine():
    sr = 44100
    t = np.linspace(0, 1, sr)
    freq = 1000
    sine = 0.5 * np.sin(2 * np.pi * freq * t)
    
    result = analyze_spectrum(sine, sr)
    
    # Centroid for a 1000Hz sine should be around 1000Hz
    assert 900 < result.spectral_centroid_avg < 1100
    # HF Cutoff should be at least 1000Hz
    assert result.hf_cutoff_hz >= 1000
