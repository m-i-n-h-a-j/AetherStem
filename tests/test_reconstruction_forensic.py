import numpy as np

from ai.reconstruction.analysis.forensic import ForensicAnalyzer
from ai.runtime.audio_buffer import AudioBuffer


def test_forensic_analysis_is_deterministic_and_transparent():
    sr = 44100
    t = np.linspace(0, 1, sr, endpoint=False)
    low_band = 0.4 * np.sin(2 * np.pi * 1000 * t)
    samples = np.vstack([low_band, low_band]).astype(np.float32)

    audio = AudioBuffer(samples=samples, sample_rate=sr, layout="channels_first")
    first = ForensicAnalyzer().analyze(audio)
    second = ForensicAnalyzer().analyze(audio)

    assert first.to_dict() == second.to_dict()
    assert "not true lossless recovery" in first.philosophy
    assert 0.0 <= first.confidence.confidence <= 1.0

