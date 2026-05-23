from __future__ import annotations

from typing import Any


class TorchBackend:
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

    def devices(self) -> list[str]:
        devices = ["cpu"]
        if self._torch is not None and self._torch.cuda.is_available():
            devices.insert(0, "cuda")
        return devices

    def select_device(self, preferred: str = "auto") -> str:
        devices = self.devices()
        if preferred != "auto" and preferred in devices:
            return preferred
        return "cuda" if "cuda" in devices else "cpu"

    def memory_summary(self) -> dict[str, Any]:
        if self._torch is None or not self._torch.cuda.is_available():
            return {"cuda_available": False}
        return {
            "cuda_available": True,
            "allocated_bytes": int(self._torch.cuda.memory_allocated()),
            "reserved_bytes": int(self._torch.cuda.memory_reserved()),
        }

    def infer(self, callable_obj: Any, *args: Any, **kwargs: Any) -> Any:
        if self._torch is None:
            return callable_obj(*args, **kwargs)
        with self._torch.no_grad():
            return callable_obj(*args, **kwargs)

