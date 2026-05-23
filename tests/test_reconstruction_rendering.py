import numpy as np
import soundfile as sf

from ai.reconstruction.rendering.renderer import UltraQualityRenderer
from ai.runtime.audio_buffer import AudioBuffer


def test_ultra_quality_renderer_writes_float_wav(tmp_path):
    samples = np.zeros((2, 128), dtype=np.float32)
    audio = AudioBuffer(samples=samples, sample_rate=44100, layout="channels_first")

    path = UltraQualityRenderer().render(audio, tmp_path / "render", target_rate=44100, output_format="wav")
    info = sf.info(path)

    assert path.exists()
    assert info.samplerate == 44100
    assert info.subtype == "FLOAT"

