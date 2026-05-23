from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import numpy as np

AudioLayout = Literal["channels_first", "channels_last", "mono"]


@dataclass(frozen=True)
class AudioBuffer:
    samples: np.ndarray
    sample_rate: int
    channels: int | None = None
    dtype: str | None = None
    layout: AudioLayout = "channels_first"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "samples", np.asarray(self.samples))
        inferred_channels = self._infer_channels()
        object.__setattr__(self, "channels", self.channels or inferred_channels)
        object.__setattr__(self, "dtype", self.dtype or str(self.samples.dtype))
        self.validate()

    @property
    def duration_seconds(self) -> float:
        return self.sample_count / self.sample_rate

    @property
    def sample_count(self) -> int:
        if self.samples.ndim == 1:
            return int(self.samples.shape[0])
        if self.layout == "channels_last":
            return int(self.samples.shape[0])
        return int(self.samples.shape[-1])

    def validate(self) -> None:
        if self.sample_rate <= 0:
            raise ValueError("sample_rate must be positive")
        if self.samples.ndim not in (1, 2):
            raise ValueError("AudioBuffer supports mono or 2D channel audio")
        if self.layout == "mono" and self.samples.ndim != 1:
            raise ValueError("mono layout requires a 1D sample array")
        if self.channels is not None and self.channels <= 0:
            raise ValueError("channels must be positive")

    def as_channels_first(self) -> "AudioBuffer":
        if self.samples.ndim == 1:
            samples = self.samples.reshape(1, -1)
        elif self.layout == "channels_last":
            samples = self.samples.T
        else:
            samples = self.samples
        return AudioBuffer(samples=samples, sample_rate=self.sample_rate, layout="channels_first", metadata=dict(self.metadata))

    def as_channels_last(self) -> "AudioBuffer":
        if self.samples.ndim == 1:
            samples = self.samples.reshape(-1, 1)
        elif self.layout == "channels_first":
            samples = self.samples.T
        else:
            samples = self.samples
        return AudioBuffer(samples=samples, sample_rate=self.sample_rate, layout="channels_last", metadata=dict(self.metadata))

    def astype(self, dtype: str | np.dtype) -> "AudioBuffer":
        return AudioBuffer(
            samples=self.samples.astype(dtype, copy=False),
            sample_rate=self.sample_rate,
            channels=self.channels,
            layout=self.layout,
            metadata=dict(self.metadata),
        )

    def _infer_channels(self) -> int:
        if self.samples.ndim == 1:
            return 1
        if self.layout == "channels_last":
            return int(self.samples.shape[1])
        return int(self.samples.shape[0])

