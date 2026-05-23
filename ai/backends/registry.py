from __future__ import annotations

from ai.backends.base import RuntimeBackend
from ai.runtime.context import ExecutionContext


class BackendRegistry:
    def __init__(self) -> None:
        self._backends: dict[str, RuntimeBackend] = {}

    def register(self, backend: RuntimeBackend) -> None:
        self._backends[backend.name] = backend

    def names(self) -> list[str]:
        return sorted(self._backends)

    def diagnostics(self) -> dict:
        return {name: backend.diagnostics() for name, backend in sorted(self._backends.items())}

    def capabilities(self) -> dict:
        return {name: backend.capabilities() for name, backend in sorted(self._backends.items())}

    def resolve(self, context: ExecutionContext) -> RuntimeBackend:
        if context.backend != "auto":
            backend = self._backends.get(context.backend)
            if backend is None:
                raise RuntimeError(f"Unknown runtime backend: {context.backend}")
            if not backend.available() and not context.fallback_to_cpu:
                raise RuntimeError(f"Runtime backend unavailable: {context.backend}")
            return backend
        for name in ("onnx", "torch"):
            backend = self._backends.get(name)
            if backend and backend.available():
                return backend
        raise RuntimeError("No runtime backend is available.")


default_backend_registry = BackendRegistry()


def _register_defaults() -> None:
    from ai.backends.onnx_runtime import OnnxRuntimeBackend
    from ai.backends.torch_runtime import TorchRuntimeBackend

    default_backend_registry.register(OnnxRuntimeBackend())
    default_backend_registry.register(TorchRuntimeBackend())


_register_defaults()
