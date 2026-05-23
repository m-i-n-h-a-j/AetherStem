from __future__ import annotations

from pathlib import Path
from typing import Any

from ai.runtime.context import ExecutionContext


class OnnxRuntimeBackend:
    name = "onnx"

    def __init__(self) -> None:
        self._ort = None
        self._sessions: dict[tuple[str, tuple[str, ...]], Any] = {}
        try:
            import onnxruntime as ort

            self._ort = ort
        except Exception:
            self._ort = None

    def available(self) -> bool:
        return self._ort is not None

    def providers(self) -> list[str]:
        if self._ort is None:
            return []
        return list(self._ort.get_available_providers())

    def diagnostics(self) -> dict[str, Any]:
        return {"available": self.available(), "providers": self.providers()}

    def capabilities(self) -> dict[str, Any]:
        providers = self.providers()
        return {
            "backend": self.name,
            "available": self.available(),
            "providers": providers,
            "precisions": ["fp32", "fp16"] if "CUDAExecutionProvider" in providers else ["fp32"],
            "features": ["session_cache", "provider_selection", "profiling_hooks"],
        }

    def prepare_context(self, context: ExecutionContext) -> ExecutionContext:
        providers = self.providers()
        requested = context.provider
        selected = None
        if requested not in ("auto", ""):
            provider_name = _provider_name(requested)
            if provider_name in providers:
                selected = provider_name
            elif not context.fallback_to_cpu:
                raise RuntimeError(f"ONNX provider unavailable: {provider_name}")
        if selected is None:
            if context.device == "cuda" and "CUDAExecutionProvider" in providers:
                selected = "CUDAExecutionProvider"
            elif "CPUExecutionProvider" in providers:
                selected = "CPUExecutionProvider"
            elif providers:
                selected = providers[0]
        if selected is None:
            raise RuntimeError("No ONNX Runtime provider is available.")
        diagnostics = dict(context.diagnostics)
        diagnostics["onnx_provider"] = selected
        if context.precision == "fp16":
            diagnostics["precision_warning"] = "fp16 requested; model conversion is not performed by v0.4 runtime."
        device = "cuda" if selected == "CUDAExecutionProvider" else "cpu"
        prepared = context.child(backend="onnx", provider=selected, device=device, diagnostics=diagnostics)
        prepared.telemetry.emit("provider_selected", backend="onnx", provider=selected, device=device)
        return prepared

    def session(self, model_path: Path, context: ExecutionContext):
        if self._ort is None:
            raise RuntimeError("onnxruntime is not installed.")
        prepared = self.prepare_context(context)
        providers = (prepared.provider,)
        key = (str(model_path), providers)
        if key not in self._sessions:
            self._sessions[key] = self._ort.InferenceSession(str(model_path), providers=list(providers))
        return self._sessions[key], prepared

    def run(self, model_path: Path, inputs: dict[str, Any], context: ExecutionContext) -> tuple[list[Any], ExecutionContext]:
        session, prepared = self.session(model_path, context)
        outputs = session.run(None, inputs)
        return outputs, prepared


def _provider_name(value: str) -> str:
    normalized = value.lower()
    if normalized in {"cpu", "cpuexecutionprovider"}:
        return "CPUExecutionProvider"
    if normalized in {"cuda", "cudaexecutionprovider"}:
        return "CUDAExecutionProvider"
    return value
