import numpy as np

from ai.reconstruction.core import ReconstructionContext, ReconstructionProfile
from ai.reconstruction.pipelines.pipeline import ReconstructionPipeline
from ai.runtime.audio_buffer import AudioBuffer


def test_reconstruction_pipeline_returns_report_and_audio():
    samples = np.vstack([
        np.linspace(-0.2, 0.2, 256, dtype=np.float32),
        np.linspace(0.2, -0.2, 256, dtype=np.float32),
    ])
    audio = AudioBuffer(samples=samples, sample_rate=44100, layout="channels_first")

    result = ReconstructionPipeline().run(audio, ReconstructionContext(profile=ReconstructionProfile.BALANCED))

    assert result.audio.sample_count == audio.sample_count
    assert result.evaluation["reconstruction_score"] >= 0.0
    assert result.profile["philosophy"] == "plausible reconstruction, not true lossless recovery"

