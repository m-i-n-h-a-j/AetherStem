import numpy as np
import pytest

from ai.runtime.audio_buffer import AudioBuffer


def test_audio_buffer_layout_conversion_preserves_duration():
    samples = np.zeros((100, 2), dtype=np.float32)
    buffer = AudioBuffer(samples=samples, sample_rate=100, layout="channels_last")

    channels_first = buffer.as_channels_first()

    assert channels_first.samples.shape == (2, 100)
    assert channels_first.channels == 2
    assert channels_first.duration_seconds == pytest.approx(1.0)


def test_audio_buffer_rejects_invalid_sample_rate():
    with pytest.raises(ValueError):
        AudioBuffer(samples=np.zeros(10), sample_rate=0, layout="mono")

