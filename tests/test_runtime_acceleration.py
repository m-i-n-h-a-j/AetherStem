from ai.backends.onnx_runtime import OnnxRuntimeBackend
from ai.optimization.runtime_profiles import RuntimeProfileSelector
from ai.runtime.context import ExecutionContext
from cli.main import _runtime_overrides


def test_runtime_profile_prefers_tensorrt_then_cuda():
    profile = RuntimeProfileSelector().select(
        "auto",
        {
            "onnx": {
                "available": True,
                "providers": ["TensorrtExecutionProvider", "CUDAExecutionProvider", "CPUExecutionProvider"],
            },
            "torch": {"available": True, "cuda_available": False},
        },
    )

    assert profile.name == "gpu_extreme"
    assert profile.device == "cuda"
    assert profile.provider == "tensorrt"


def test_runtime_profile_prefers_cuda_without_tensorrt():
    profile = RuntimeProfileSelector().select(
        "auto",
        {
            "onnx": {"available": True, "providers": ["CUDAExecutionProvider", "CPUExecutionProvider"]},
            "torch": {"available": True, "cuda_available": True},
        },
    )

    assert profile.name == "cuda_fast"
    assert profile.device == "cuda"
    assert profile.provider == "cuda"


def test_onnx_prepare_context_records_provider_candidates():
    backend = OnnxRuntimeBackend()
    backend.providers = lambda: ["TensorrtExecutionProvider", "CUDAExecutionProvider", "CPUExecutionProvider"]  # type: ignore[method-assign]

    prepared = backend.prepare_context(ExecutionContext(backend="onnx", device="cuda", provider="auto"))

    assert prepared.device == "cuda"
    assert prepared.provider == "TensorrtExecutionProvider"
    assert prepared.diagnostics["onnx_provider_candidates"] == [
        "TensorrtExecutionProvider",
        "CUDAExecutionProvider",
        "CPUExecutionProvider",
    ]


def test_cli_cuda_request_disables_silent_cpu_fallback():
    overrides = _runtime_overrides("onnx", "cuda", None, None, False)

    assert overrides["device"] == "cuda"
    assert overrides["fallback_to_cpu"] is False
