from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeProfile:
    name: str
    backend: str
    device: str
    provider: str
    precision: str
    low_memory: bool
    fallback_to_cpu: bool
    reason: str


class RuntimeProfileSelector:
    def select(self, requested: str = "auto", diagnostics: dict | None = None) -> RuntimeProfile:
        diagnostics = diagnostics or {}
        if requested and requested != "auto":
            return _profile(requested)
        torch_diag = diagnostics.get("torch", {})
        onnx_diag = diagnostics.get("onnx", {})
        providers = onnx_diag.get("providers", [])
        if "TensorrtExecutionProvider" in providers:
            return _profile("gpu_extreme")
        if "CUDAExecutionProvider" in providers or torch_diag.get("cuda_available"):
            return _profile("cuda_fast")
        if onnx_diag.get("available") or "CPUExecutionProvider" in providers:
            return _profile("cpu_safe")
        return _profile("portable")


def _profile(name: str) -> RuntimeProfile:
    profiles = {
        "gpu_extreme": RuntimeProfile("gpu_extreme", "onnx", "cuda", "tensorrt", "fp16", False, True, "TensorRT-preferred GPU execution with CUDA fallback"),
        "cpu_safe": RuntimeProfile("cpu_safe", "onnx", "cpu", "cpu", "fp32", False, True, "portable CPU ONNX execution"),
        "cuda_fast": RuntimeProfile("cuda_fast", "onnx", "cuda", "cuda", "fp16", False, True, "CUDA-preferred fast execution"),
        "cuda_low_memory": RuntimeProfile("cuda_low_memory", "onnx", "cuda", "cuda", "fp16", True, True, "CUDA with conservative memory use"),
        "portable": RuntimeProfile("portable", "auto", "cpu", "auto", "fp32", True, True, "maximum compatibility"),
        "diagnostic": RuntimeProfile("diagnostic", "auto", "cpu", "auto", "fp32", True, True, "diagnostic-safe execution"),
    }
    if name not in profiles:
        raise KeyError(f"Unknown runtime profile: {name}")
    return profiles[name]
