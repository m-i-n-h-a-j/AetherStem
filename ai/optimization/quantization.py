from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class QuantizationMetadata:
    mode: str = "none"
    dtype: str = "int8"
    calibration_required: bool = False
    compatible_backends: tuple[str, ...] = ()
    notes: str = ""
    parameters: dict = field(default_factory=dict)

