import numpy as np

from ai.runtime.audio_buffer import AudioBuffer
from ai.runtime.chunk_scheduler import ChunkScheduler, overlap_add


def test_chunk_scheduler_preserves_duration_with_padding():
    audio = AudioBuffer(samples=np.ones((2, 25), dtype=np.float32), sample_rate=25, layout="channels_first")
    plan = ChunkScheduler().plan(audio, chunk_size=10, overlap_ratio=0.2)

    reconstructed = overlap_add([(chunk, chunk.samples) for chunk in plan.chunks], plan.total_samples)

    assert reconstructed.shape == (2, 25)
    assert np.allclose(reconstructed, audio.samples)


def test_low_memory_scheduler_uses_sequential_batching():
    audio = AudioBuffer(samples=np.ones((2, 100), dtype=np.float32), sample_rate=100, layout="channels_first")
    plan = ChunkScheduler().plan(audio, chunk_size=20, overlap_ratio=0.25, available_memory_mb=1000, low_memory=True)

    assert plan.batch_size == 1

