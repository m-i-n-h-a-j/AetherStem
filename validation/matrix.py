from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import product
from typing import Iterable


@dataclass(frozen=True)
class ValidationCase:
    pipeline: str
    backend: str
    precision: str
    quality: str
    device: str
    chunk_size: int
    streaming: bool

    def id(self) -> str:
        mode = "stream" if self.streaming else "offline"
        return f"{self.pipeline}-{self.backend}-{self.precision}-{self.quality}-{self.device}-{self.chunk_size}-{mode}"

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def default_validation_matrix(
    pipelines: Iterable[str] = ("reconstruct", "upscale", "remaster"),
    backends: Iterable[str] = ("numpy", "torch", "onnx"),
    precisions: Iterable[str] = ("fp32", "fp16", "mixed"),
    qualities: Iterable[str] = ("safe", "balanced", "forensic"),
    devices: Iterable[str] = ("cpu", "cuda"),
    chunk_sizes: Iterable[int] = (262144, 441000),
    streaming_modes: Iterable[bool] = (False, True),
) -> list[ValidationCase]:
    return [
        ValidationCase(*values)
        for values in product(pipelines, backends, precisions, qualities, devices, chunk_sizes, streaming_modes)
    ]
