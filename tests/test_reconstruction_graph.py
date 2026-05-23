import numpy as np

from ai.reconstruction.analysis.forensic import ForensicAnalyzer
from ai.reconstruction.core import ReconstructionProfile
from ai.reconstruction.orchestration.builder import ReconstructionGraphBuilder
from ai.runtime.audio_buffer import AudioBuffer


def test_reconstruction_graph_generation_is_reproducible():
    samples = np.ones((2, 128), dtype=np.float32) * 0.5
    audio = AudioBuffer(samples=samples, sample_rate=44100, layout="channels_first")
    report = ForensicAnalyzer().analyze(audio)

    first = ReconstructionGraphBuilder().build(report, ReconstructionProfile.EXTREME)
    second = ReconstructionGraphBuilder().build(report, ReconstructionProfile.EXTREME)

    assert [stage.name for stage in first.stages] == [stage.name for stage in second.stages]
    assert "mastering" in [stage.name for stage in first.stages]

