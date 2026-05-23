from __future__ import annotations

from ai.runtime.context import ExecutionContext


class DemucsTorchFallback:
    async def load(self, context: ExecutionContext) -> None:
        try:
            import torch  # noqa: F401
        except Exception as exc:
            raise RuntimeError("PyTorch fallback requested but torch is unavailable.") from exc

