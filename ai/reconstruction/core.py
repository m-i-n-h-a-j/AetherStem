from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

from ai.runtime.context import ExecutionContext


class ReconstructionProfile(StrEnum):
    FAST = "fast"
    BALANCED = "balanced"
    EXTREME = "extreme"
    ARCHIVAL = "archival"
    EXPERIMENTAL = "experimental"


class MasteringProfile(StrEnum):
    TRANSPARENT = "transparent"
    HIFI = "hifi"
    CINEMATIC = "cinematic"
    STUDIO = "studio"
    ARCHIVAL = "archival"


@dataclass
class ReconstructionContext:
    profile: ReconstructionProfile = ReconstructionProfile.BALANCED
    mastering_profile: MasteringProfile = MasteringProfile.TRANSPARENT
    target_rate: int = 192000
    output_format: str = "wav"
    multi_pass: bool = False
    harmonic_reconstruction: bool = False
    bandwidth_extension: bool = False
    output_dir: Path = Path("exports")
    runtime: ExecutionContext = field(default_factory=ExecutionContext)
    options: dict[str, Any] = field(default_factory=dict)


@dataclass
class StageResult:
    stage: str
    audio: Any
    diagnostics: dict[str, Any] = field(default_factory=dict)

