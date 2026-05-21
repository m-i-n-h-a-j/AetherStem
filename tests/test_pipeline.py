import numpy as np
import pytest
import soundfile as sf
from pathlib import Path
from pipeline.runner import PipelineRunner
from utils.config_loader import config

def test_pipeline_runner_end_to_end(tmp_path):
    # Setup: Create a temporary stereo WAV file (2 seconds at 44100Hz)
    sr = 44100
    duration = 2.0
    half_samples = int(sr * (duration / 2))
    t = np.linspace(0, duration / 2, half_samples, endpoint=False)
    # Generate 1000Hz sine wave for Left and 1200Hz for Right for the first half
    left_sine = 0.5 * np.sin(2 * np.pi * 1000 * t)
    right_sine = 0.5 * np.sin(2 * np.pi * 1200 * t)
    # Silence for the second half to test noise floor
    left = np.concatenate([left_sine, np.zeros(half_samples)])
    right = np.concatenate([right_sine, np.zeros(half_samples)])
    signal = np.vstack([left, right]).T.astype(np.float32)
    
    input_file = tmp_path / "test_stereo_input.wav"
    sf.write(input_file, signal, sr)
    
    # Run the pipeline
    output_dir = tmp_path / "output_reports"
    runner = PipelineRunner(output_dir=output_dir)
    result = runner.run(input_file)
    
    # Assertions
    assert result.success is True
    assert result.error is None
    
    # Check Metadata
    assert result.metadata.filename == "test_stereo_input.wav"
    assert result.metadata.channels == 2
    assert result.metadata.sample_rate == sr
    assert result.metadata.duration == pytest.approx(duration, abs=0.1)
    
    # Check Analysis exists and is populated
    assert result.analysis is not None
    assert result.analysis.loudness.integrated_lufs < 0.0
    assert result.analysis.stereo.is_mono is False
    assert result.analysis.clipping_count == 0
    assert result.analysis.noise_floor_db < -60.0
    
    # Check Quality Detection
    assert result.quality is not None
    
    # Check Artifacts are generated
    assert "spectrogram" in result.artifacts
    assert "waveform" in result.artifacts
    assert "vectorscope" in result.artifacts
    assert "phase_correlation_graph" in result.artifacts
    assert "report" in result.artifacts
    
    # Check physical files exist
    assert Path(result.artifacts["spectrogram"]).exists()
    assert Path(result.artifacts["waveform"]).exists()
    assert Path(result.artifacts["vectorscope"]).exists()
    assert Path(result.artifacts["phase_correlation_graph"]).exists()
    assert Path(result.artifacts["report"]).exists()

    # Clean up generated artifacts
    for art_path in result.artifacts.values():
        p = Path(art_path)
        if p.exists():
            p.unlink()
