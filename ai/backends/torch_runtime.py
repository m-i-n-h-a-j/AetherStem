from __future__ import annotations

from typing import Any

from ai.runtime.context import ExecutionContext


class TorchRuntimeBackend:
    name = "torch"

    def __init__(self) -> None:
        self._torch = None
        try:
            import torch

            self._torch = torch
        except Exception:
            self._torch = None

    def available(self) -> bool:
        return self._torch is not None

    def diagnostics(self) -> dict[str, Any]:
        return {
            "available": self.available(),
            "cuda_available": bool(self._torch is not None and self._torch.cuda.is_available()),
        }

    def prepare_context(self, context: ExecutionContext) -> ExecutionContext:
        if self._torch is None:
            raise RuntimeError("torch is not installed.")
        cuda_available = self._torch.cuda.is_available()
        if context.device == "cuda" and not cuda_available and not context.fallback_to_cpu:
            raise RuntimeError("CUDA requested but unavailable for torch runtime.")
        device = "cuda" if (context.device in {"auto", "cuda"} and cuda_available) else "cpu"
        diagnostics = dict(context.diagnostics)
        diagnostics["torch_device"] = device
        return context.child(backend="torch", device=device, provider=device, diagnostics=diagnostics)

