from __future__ import annotations

from typing import Any


class OnnxBackend:
    name = "onnx"

    def __init__(self) -> None:
        self._ort = None
        try:
            import onnxruntime as ort

            self._ort = ort
        except Exception:
            self._ort = None

    def available(self) -> bool:
        return self._ort is not None

    def devices(self) -> list[str]:
        if self._ort is None:
            return []
        providers = self._ort.get_available_providers()
        devices = []
        if "CUDAExecutionProvider" in providers:
            devices.append("cuda")
        if "CPUExecutionProvider" in providers:
            devices.append("cpu")
        return devices or ["cpu"]

    def select_device(self, preferred: str = "auto") -> str:
        devices = self.devices()
        if preferred != "auto" and preferred in devices:
            return preferred
        return "cuda" if "cuda" in devices else "cpu"

    def memory_summary(self) -> dict[str, Any]:
        return {"providers": self._ort.get_available_providers() if self._ort else []}

    def infer(self, callable_obj: Any, *args: Any, **kwargs: Any) -> Any:
        return callable_obj(*args, **kwargs)

