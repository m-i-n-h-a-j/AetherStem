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
        providers = self.providers()
        return {
            "available": self.available(),
            "providers": providers,
            "cuda_provider_available": "CUDAExecutionProvider" in providers,
            "tensorrt_provider_available": "TensorrtExecutionProvider" in providers,
            "provider_priority": _provider_candidates("auto", "auto", providers),
        }

    def capabilities(self) -> dict[str, Any]:
        providers = self.providers()
        return {
            "backend": self.name,
            "available": self.available(),
            "providers": providers,
            "precisions": ["fp32", "fp16"] if "CUDAExecutionProvider" in providers else ["fp32"],
            "features": ["session_cache", "provider_selection", "provider_fallback", "profiling_hooks"],
        }

    def prepare_context(self, context: ExecutionContext) -> ExecutionContext:
        providers = self.providers()
        candidates = _provider_candidates(context.provider, context.device, providers)
        selected = candidates[0] if candidates else None
        if selected is None:
            raise RuntimeError("No ONNX Runtime provider is available.")
        diagnostics = dict(context.diagnostics)
        diagnostics["onnx_available_providers"] = providers
        diagnostics["onnx_provider_candidates"] = candidates
        diagnostics["onnx_provider"] = selected
        if context.device == "cuda" and selected == "CPUExecutionProvider":
            diagnostics["runtime_warning"] = "CUDA was requested but ONNX selected CPUExecutionProvider."
            if not context.fallback_to_cpu:
                raise RuntimeError("CUDA requested but no ONNX CUDA/TensorRT provider is available.")
        if context.precision == "fp16":
            diagnostics["precision_warning"] = "fp16 requested; model conversion is not performed by v0.4 runtime."
        device = "cuda" if selected in {"CUDAExecutionProvider", "TensorrtExecutionProvider"} else "cpu"
        prepared = context.child(backend="onnx", provider=selected, device=device, diagnostics=diagnostics)
        prepared.telemetry.emit("provider_selected", backend="onnx", provider=selected, device=device, candidates=candidates)
        return prepared

    def session(self, model_path: Path, context: ExecutionContext):
        if self._ort is None:
            raise RuntimeError("onnxruntime is not installed.")
        prepared = self.prepare_context(context)
        candidates = prepared.diagnostics.get("onnx_provider_candidates", [prepared.provider])
        errors: list[dict[str, str]] = []
        for provider in candidates:
            key = (str(model_path), (provider,))
            try:
                if key not in self._sessions:
                    self._sessions[key] = self._ort.InferenceSession(str(model_path), providers=[provider])
                actual_provider = self._sessions[key].get_providers()[0] if self._sessions[key].get_providers() else provider
                if actual_provider != provider:
                    raise RuntimeError(f"Requested {provider}, but ONNX Runtime initialized {actual_provider}.")
                diagnostics = dict(prepared.diagnostics)
                diagnostics["onnx_provider"] = provider
                if errors:
                    diagnostics["onnx_provider_failures"] = errors
                device = "cuda" if provider in {"CUDAExecutionProvider", "TensorrtExecutionProvider"} else "cpu"
                selected = prepared.child(provider=provider, device=device, diagnostics=diagnostics)
                if provider == "CPUExecutionProvider" and context.device == "cuda":
                    selected.telemetry.emit("fallback_triggered", reason="onnx_gpu_provider_failed", target="CPUExecutionProvider", failures=errors)
                    if not context.fallback_to_cpu:
                        raise RuntimeError(f"ONNX CUDA providers failed: {errors}")
                selected.telemetry.emit("provider_selected", backend="onnx", provider=provider, device=device, failures=errors)
                return self._sessions[key], selected
            except Exception as exc:
                errors.append({"provider": provider, "error": str(exc)})
                if provider == "TensorrtExecutionProvider":
                    prepared.telemetry.emit("provider_failed", backend="onnx", provider=provider, reason="tensorrt_initialization_failed", error=str(exc))
                if provider != "CPUExecutionProvider":
                    continue
                raise RuntimeError(f"ONNX provider initialization failed: {errors}") from exc
        raise RuntimeError(f"No ONNX Runtime provider could initialize: {errors}")

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
    if normalized in {"tensorrt", "trt", "tensorrtexecutionprovider"}:
        return "TensorrtExecutionProvider"
    return value


def _provider_candidates(requested: str, device: str, providers: list[str]) -> list[str]:
    if not providers:
        return []
    if requested not in ("auto", ""):
        preferred = _provider_name(requested)
        ordered = [preferred]
        if preferred == "TensorrtExecutionProvider":
            ordered.append("CUDAExecutionProvider")
        if device != "cuda":
            ordered.append("CPUExecutionProvider")
        else:
            ordered.extend(["CUDAExecutionProvider", "CPUExecutionProvider"])
        return _dedupe([provider for provider in ordered if provider in providers])
    if device == "cpu":
        return ["CPUExecutionProvider"] if "CPUExecutionProvider" in providers else []
    ordered = ["TensorrtExecutionProvider", "CUDAExecutionProvider", "CPUExecutionProvider"]
    return [provider for provider in ordered if provider in providers]


def _dedupe(values: list[str]) -> list[str]:
    seen = set()
    result = []
    for value in values:
        if value not in seen:
            result.append(value)
            seen.add(value)
    return result
