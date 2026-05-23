from __future__ import annotations

from typing import Protocol

import numpy as np


class StreamingProcessor(Protocol):
    def push(self, audio: np.ndarray, sample_rate: int) -> None:
        ...

    def flush(self) -> np.ndarray:
        ...

