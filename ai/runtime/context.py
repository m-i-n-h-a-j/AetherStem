from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ai.runtime.cancellation import CancellationToken
from ai.runtime.progress import ProgressReporter
from ai.telemetry.profiler import RuntimeProfiler
from ai.telemetry.tracer import RuntimeTracer


@dataclass
class ExecutionContext:
    backend: str = "auto"
    device: str = "auto"
    provider: str = "auto"
    precision: str = "fp32"
    low_memory: bool = False
    fallback_to_cpu: bool = True
    diagnostics: dict[str, Any] = field(default_factory=dict)
    progress: ProgressReporter = field(default_factory=ProgressReporter)
    cancellation: CancellationToken = field(default_factory=CancellationToken)
    telemetry: RuntimeTracer = field(default_factory=RuntimeTracer)
    profiler: RuntimeProfiler = field(default_factory=RuntimeProfiler)

    def child(self, **updates) -> "ExecutionContext":
        values = {
            "backend": self.backend,
            "device": self.device,
            "provider": self.provider,
            "precision": self.precision,
            "low_memory": self.low_memory,
            "fallback_to_cpu": self.fallback_to_cpu,
            "diagnostics": dict(self.diagnostics),
            "progress": self.progress,
            "cancellation": self.cancellation,
            "telemetry": self.telemetry,
            "profiler": self.profiler,
        }
        values.update(updates)
        return ExecutionContext(**values)
