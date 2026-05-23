from __future__ import annotations

from pathlib import Path

import librosa
import numpy as np
import soundfile as sf

from ai.runtime.audio_buffer import AudioBuffer


class UltraQualityRenderer:
    def render(
        self,
        audio: AudioBuffer,
        output_path: Path,
        target_rate: int = 192000,
        output_format: str = "wav",
    ) -> Path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        samples = audio.as_channels_first().samples.astype(np.float32, copy=True)
        peak = float(np.max(np.abs(samples))) if samples.size else 0.0
        if peak > 0.98:
            samples *= 0.98 / peak
        if target_rate != audio.sample_rate:
            samples = np.vstack([librosa.resample(channel, orig_sr=audio.sample_rate, target_sr=target_rate, res_type="soxr_hq") for channel in samples]).astype(np.float32)
        suffix = output_format.lower().lstrip(".")
        path = output_path.with_suffix(f".{suffix}")
        sf.write(path, samples.T, target_rate, subtype="FLOAT")
        return path

