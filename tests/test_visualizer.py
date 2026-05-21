import numpy as np
import pytest
from pathlib import Path
from dsp.visualizer import (
    generate_spectrogram,
    generate_waveform,
    generate_vectorscope,
    generate_phase_correlation_graph
)

def test_visualizers(tmp_path):
    # Setup stereo signal: 1 second at 44100Hz
    sr = 44100
    t = np.linspace(0, 1.0, sr, endpoint=False)
    left = 0.5 * np.sin(2 * np.pi * 440 * t)
    right = 0.5 * np.cos(2 * np.pi * 440 * t) # Phase offset for stereo width
    signal = np.vstack([left, right]).astype(np.float32)
    
    spec_path = tmp_path / "test_spectrogram.png"
    wave_path = tmp_path / "test_waveform.png"
    vector_path = tmp_path / "test_vectorscope.png"
    phase_path = tmp_path / "test_phase.png"
    
    # Run generators
    generate_spectrogram(signal, sr, spec_path)
    generate_waveform(signal, sr, wave_path)
    generate_vectorscope(signal, vector_path)
    generate_phase_correlation_graph(signal, sr, phase_path)
    
    # Assert files exist and have content
    assert spec_path.exists()
    assert spec_path.stat().st_size > 0
    
    assert wave_path.exists()
    assert wave_path.stat().st_size > 0
    
    assert vector_path.exists()
    assert vector_path.stat().st_size > 0
    
    assert phase_path.exists()
    assert phase_path.stat().st_size > 0
