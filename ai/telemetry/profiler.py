from __future__ import annotations

from contextlib import contextmanager
from time import perf_counter
from typing import Any, Iterator


class RuntimeProfiler:
    def __init__(self) -> None:
        self.spans: list[dict[str, Any]] = []

    @contextmanager
    def span(self, name: str, **metadata: Any) -> Iterator[None]:
        started = perf_counter()
        try:
            yield
        finally:
            self.spans.append({"name": name, "duration_ms": (perf_counter() - started) * 1000, "metadata": metadata})

    def report(self) -> dict[str, Any]:
        total = sum(span["duration_ms"] for span in self.spans)
        return {"total_profiled_ms": total, "spans": self.spans}

