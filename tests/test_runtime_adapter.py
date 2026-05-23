import numpy as np

from ai.adapters.separation import SeparationOptions
from ai.models.demucs.runtime_adapter import DemucsRuntimeAdapter
from ai.runtime.audio_buffer import AudioBuffer
from ai.runtime.context import ExecutionContext
from ai.runtime.executor import RuntimeExecutor


def test_demucs_runtime_adapter_outputs_stereo_stems_with_input_duration():
    sr = 100
    samples = np.vstack([
        np.linspace(-0.5, 0.5, 100, dtype=np.float32),
        np.linspace(0.5, -0.5, 100, dtype=np.float32),
    ])
    adapter = DemucsRuntimeAdapter()
    context = ExecutionContext(low_memory=True)
    audio = AudioBuffer(samples=samples, sample_rate=sr, layout="channels_first")
    options = SeparationOptions(stems=["vocals", "drums", "bass", "other"], chunk_size=32, overlap=0.25)

    result = RuntimeExecutor().run(adapter.separate(audio, context, options))

    assert set(result.stems) == {"vocals", "drums", "bass", "other"}
    for stem in result.stems.values():
        assert stem.audio.samples.shape == (2, 100)
        assert stem.audio.sample_rate == sr
    assert result.diagnostics["chunks"] > 1

