from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True, slots=True)
class TensorSignature:
    name: str
    shape: tuple[int | str, ...]
    dtype: str = "float32"
    layout: str = "bcs"
    semantics: str = "audio"


@dataclass(frozen=True, slots=True)
class PrecisionSupport:
    precision: str
    backends: tuple[str, ...]
    requires_calibration: bool = False
    notes: str = ""


@dataclass(frozen=True, slots=True)
class ModelAsset:
    path: str | None = None
    url: str | None = None
    cache_key: str | None = None
    sha256: str | None = None
    size_bytes: int | None = None


@dataclass(frozen=True, slots=True)
class ModelManifest:
    id: str
    version: str
    architecture: str
    task: str
    supported_backends: tuple[str, ...]
    supported_precisions: tuple[str, ...]
    sample_rate: int
    channels: int
    stems: tuple[str, ...] = ()
    sha256: str = ""
    model_format: str = "onnx"
    name: str | None = None
    description: str = ""
    license: str | None = None
    source_url: str | None = None
    minimum_runtime_version: str = "0.5.0"
    input_signature: TensorSignature | None = None
    output_signature: TensorSignature | None = None
    asset: ModelAsset | None = None
    quantization: dict[str, Any] = field(default_factory=dict)
    memory_hints: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ResolvedModel:
    manifest: ModelManifest
    asset_path: Path | None
    backend: str
    device: str
    precision: str
    diagnostics: dict[str, Any] = field(default_factory=dict)

