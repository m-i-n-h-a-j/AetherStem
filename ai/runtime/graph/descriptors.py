from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class RuntimeNodeDescriptor:
    name: str
    cpu_cost: float
    vram_cost_mb: float
    latency_ms: float
    precision: str = "fp32"
    parallelizable: bool = False
    deterministic: bool = True
    dependencies: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RuntimeGraphDescriptor:
    nodes: tuple[RuntimeNodeDescriptor, ...] = field(default_factory=tuple)

    def fingerprint(self) -> str:
        import hashlib
        import json

        payload = [node.to_dict() for node in sorted(self.nodes, key=lambda item: item.name)]
        return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()

    def total_vram_mb(self) -> float:
        return float(sum(node.vram_cost_mb for node in self.nodes))

    def deterministic(self) -> bool:
        return all(node.deterministic for node in self.nodes)
