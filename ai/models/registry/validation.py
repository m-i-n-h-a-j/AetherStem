from __future__ import annotations

import re
from typing import Any

from ai.models.registry.metadata import ModelAsset, ModelManifest, TensorSignature

SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?$")


def validate_semver(version: str) -> bool:
    return bool(SEMVER.match(version))


def manifest_from_dict(data: dict[str, Any]) -> ModelManifest:
    required = [
        "id",
        "version",
        "architecture",
        "task",
        "supported_backends",
        "supported_precisions",
        "sample_rate",
        "channels",
        "model_format",
    ]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"Manifest missing required keys: {missing}")
    if not validate_semver(str(data["version"])):
        raise ValueError(f"Manifest version must be semantic: {data['version']}")
    input_signature = _signature(data.get("input_signature"))
    output_signature = _signature(data.get("output_signature"))
    asset = _asset(data.get("asset"))
    return ModelManifest(
        id=str(data["id"]),
        version=str(data["version"]),
        architecture=str(data["architecture"]),
        task=str(data["task"]),
        supported_backends=tuple(str(item) for item in data["supported_backends"]),
        supported_precisions=tuple(str(item) for item in data["supported_precisions"]),
        sample_rate=int(data["sample_rate"]),
        channels=int(data["channels"]),
        stems=tuple(str(item) for item in data.get("stems", ())),
        sha256=str(data.get("sha256", "")),
        model_format=str(data["model_format"]),
        name=data.get("name"),
        description=str(data.get("description", "")),
        license=data.get("license"),
        source_url=data.get("source_url"),
        minimum_runtime_version=str(data.get("minimum_runtime_version", "0.5.0")),
        input_signature=input_signature,
        output_signature=output_signature,
        asset=asset,
        quantization=dict(data.get("quantization", {})),
        memory_hints=dict(data.get("memory_hints", {})),
    )


def _signature(data: dict[str, Any] | None) -> TensorSignature | None:
    if not data:
        return None
    return TensorSignature(
        name=str(data["name"]),
        shape=tuple(data.get("shape", ())),
        dtype=str(data.get("dtype", "float32")),
        layout=str(data.get("layout", "bcs")),
        semantics=str(data.get("semantics", "audio")),
    )


def _asset(data: dict[str, Any] | None) -> ModelAsset | None:
    if not data:
        return None
    return ModelAsset(
        path=data.get("path"),
        url=data.get("url"),
        cache_key=data.get("cache_key"),
        sha256=data.get("sha256"),
        size_bytes=data.get("size_bytes"),
    )

