from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class BackendSelection:
    backend: str
    device: str
    diagnostics: dict[str, Any]


class ComputeBackend(Protocol):
    name: str

    def available(self) -> bool:
        ...

    def devices(self) -> list[str]:
        ...

    def select_device(self, preferred: str = "auto") -> str:
        ...

    def memory_summary(self) -> dict[str, Any]:
        ...

    def infer(self, callable_obj: Any, *args: Any, **kwargs: Any) -> Any:
        ...


def select_backend(preferred_backend: str = "auto", preferred_device: str = "auto") -> BackendSelection:
    from ai.compute.onnx_backend import OnnxBackend
    from ai.compute.torch_backend import TorchBackend

    backends = [OnnxBackend(), TorchBackend()]
    if preferred_backend != "auto":
        backends = [backend for backend in backends if backend.name == preferred_backend]

    for backend in backends:
        if backend.available():
            device = backend.select_device(preferred_device)
            return BackendSelection(
                backend=backend.name,
                device=device,
                diagnostics={"available_devices": backend.devices(), "memory": backend.memory_summary()},
            )
    return BackendSelection(
        backend="torch",
        device="cpu",
        diagnostics={"fallback": "No preferred backend available; using CPU placeholder execution."},
    )
