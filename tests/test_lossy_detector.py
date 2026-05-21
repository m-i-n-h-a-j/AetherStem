import numpy as np
import pytest
from dsp.lossy_detector import detect_lossy

def test_detect_lossy_lowpass():
    sr = 44100
    # Create white noise and lowpass filter it at 15kHz (simulating 128kbps)
    noise = np.random.normal(0, 0.1, sr)
    
    # Simple brickwall lowpass in frequency domain
    fft = np.fft.rfft(noise)
    freqs = np.fft.rfftfreq(sr, d=1/sr)
    fft[freqs > 15000] = 0
    filtered_noise = np.fft.irfft(fft)
    
    result = detect_lossy(filtered_noise, sr)
    
    assert result.is_transcoded is True
    assert "128kbps" in result.estimate.value
