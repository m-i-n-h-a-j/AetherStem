from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ai.models.metadata import ModelMetadata
from ai.runtime.audio_buffer import AudioBuffer


@dataclass
class RuntimeStem:
    name: str
    audio: AudioBuffer
    diagnostics: dict[str, Any] = field(default_factory=dict)


@dataclass
class RuntimeAdapterResult:
    metadata: ModelMetadata
    audio: AudioBuffer | None = None
    stems: dict[str, RuntimeStem] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    diagnostics: dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0

