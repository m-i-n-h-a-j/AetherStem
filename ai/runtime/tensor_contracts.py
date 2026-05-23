from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

from ai.runtime.audio_buffer import AudioBuffer

TensorLayout = Literal["bcs", "bs c", "cs"]


@dataclass(frozen=True)
class TensorContract:
    layout: str = "bcs"
    dtype: str = "float32"
    add_batch: bool = True

    def from_audio(self, audio: AudioBuffer) -> np.ndarray:
        samples = audio.as_channels_first().samples.astype(self.dtype, copy=False)
        if self.add_batch:
            samples = samples[np.newaxis, ...]
        return samples

    def to_audio(self, tensor: np.ndarray, sample_rate: int) -> AudioBuffer:
        array = np.asarray(tensor)
        if array.ndim == 3 and array.shape[0] == 1:
            array = array[0]
        return AudioBuffer(samples=array, sample_rate=sample_rate, layout="channels_first")


def to_torch(tensor: np.ndarray, device: str = "cpu"):
    import torch

    return torch.from_numpy(np.asarray(tensor)).to(device)


def from_torch(tensor) -> np.ndarray:
    return tensor.detach().cpu().numpy()

