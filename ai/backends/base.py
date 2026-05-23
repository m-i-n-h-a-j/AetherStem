from __future__ import annotations

from typing import Any, Protocol

from ai.runtime.context import ExecutionContext


class RuntimeBackend(Protocol):
    name: str

    def available(self) -> bool:
        ...

    def diagnostics(self) -> dict[str, Any]:
        ...

    def capabilities(self) -> dict[str, Any]:
        ...

    def prepare_context(self, context: ExecutionContext) -> ExecutionContext:
        ...
