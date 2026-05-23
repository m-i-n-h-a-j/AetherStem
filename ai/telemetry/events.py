from __future__ import annotations

from dataclasses import dataclass, field
from time import time
from typing import Any


@dataclass(frozen=True)
class RuntimeEvent:
    name: str
    timestamp: float = field(default_factory=time)
    payload: dict[str, Any] = field(default_factory=dict)

