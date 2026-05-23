from __future__ import annotations

from enum import StrEnum
from typing import Any

import numpy as np
from pydantic import BaseModel, ConfigDict, Field


class ModelCapability(StrEnum):
    SEPARATE = "separate"
    DENOISE = "denoise"
    DECLIP = "declip"
    ENHANCE = "enhance"
    BANDWIDTH_EXTENSION = "bandwidth_extension"
    SUPER_RESOLUTION = "super_resolution"


class ModelCapabilities(BaseModel):
    separate: bool = False
    denoise: bool = False
    declip: bool = False
    enhance: bool = False
    bandwidth_extension: bool = False
    super_resolution: bool = False
    stems: list[str] = Field(default_factory=list)

    def has(self, capability: ModelCapability | str) -> bool:
        key = capability.value if isinstance(capability, ModelCapability) else capability
        return bool(getattr(self, key, False))


class ModelRequirements(BaseModel):
    backends: list[str] = Field(default_factory=lambda: ["torch"])
    devices: list[str] = Field(default_factory=lambda: ["cpu"])
    min_sample_rate: int | None = None
    max_channels: int | None = None
    dependencies: list[str] = Field(default_factory=list)
    model_files: list[str] = Field(default_factory=list)


class ModelCompatibility(BaseModel):
    compatible: bool
    backend: str | None = None
    device: str | None = None
    reason: str | None = None
    warnings: list[str] = Field(default_factory=list)


class ModelMetadata(BaseModel):
    name: str
    version: str
    family: str
    capabilities: ModelCapabilities
    requirements: ModelRequirements = Field(default_factory=ModelRequirements)
    description: str = ""
    source: str | None = None
    tags: list[str] = Field(default_factory=list)


class StemResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    audio: np.ndarray
    sample_rate: int
    diagnostics: dict[str, Any] = Field(default_factory=dict)


class ModelResult(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    audio: np.ndarray | None = None
    stems: dict[str, StemResult] = Field(default_factory=dict)
    sample_rate: int
    model: ModelMetadata
    backend: str
    device: str
    duration_ms: float = 0.0
    warnings: list[str] = Field(default_factory=list)
    diagnostics: dict[str, Any] = Field(default_factory=dict)

