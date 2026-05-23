from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BackendCandidate:
    name: str
    available: bool
    device: str
    throughput_score: float
    memory_score: float
    deterministic: bool = True


class BackendSelector:
    def select(self, candidates: list[BackendCandidate], require_deterministic: bool = True) -> BackendCandidate:
        available = [
            candidate
            for candidate in candidates
            if candidate.available and (candidate.deterministic or not require_deterministic)
        ]
        if not available:
            raise RuntimeError("No compatible backend candidate is available")
        return max(available, key=lambda item: (item.throughput_score * 0.6 + item.memory_score * 0.4, item.name))
