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
        cuda_available = bool(self._torch is not None and self._torch.cuda.is_available())
        return {
            "available": self.available(),
            "cuda_available": cuda_available,
            "cuda_built": bool(self._torch is not None and self._torch.backends.cuda.is_built()),
            "cuda_version": getattr(getattr(self._torch, "version", None), "cuda", None) if self._torch is not None else None,
            "device_count": int(self._torch.cuda.device_count()) if cuda_available else 0,
            "devices": [
                self._torch.cuda.get_device_name(index)
                for index in range(self._torch.cuda.device_count())
            ] if cuda_available else [],
            "fallback_reason": None if cuda_available else "torch CUDA is unavailable; install a CUDA-enabled torch wheel or use ONNX CUDA provider.",
        }

    def capabilities(self) -> dict[str, Any]:
        cuda = bool(self._torch is not None and self._torch.cuda.is_available())
        return {
            "backend": self.name,
            "available": self.available(),
            "providers": ["cuda", "cpu"] if cuda else ["cpu"] if self.available() else [],
            "precisions": ["fp32", "fp16"] if cuda else ["fp32"],
            "features": ["fallback_boundary"],
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
        if context.device == "cuda" and device == "cpu":
            diagnostics["runtime_warning"] = "CUDA was requested but torch selected CPU."
        prepared = context.child(backend="torch", device=device, provider=device, diagnostics=diagnostics)
        prepared.telemetry.emit("provider_selected", backend="torch", provider=device, device=device)
        return prepared
