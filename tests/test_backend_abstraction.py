from ai.compute.backend import select_backend
from ai.compute.tensor_rt_backend import TensorRTBackend


def test_backend_selection_falls_back_to_cpu_shape():
    selection = select_backend("auto", "auto")

    assert selection.backend in {"torch", "onnx"}
    assert selection.device in {"cpu", "cuda"}
    assert isinstance(selection.diagnostics, dict)


def test_tensorrt_backend_is_explicitly_unsupported():
    backend = TensorRTBackend()

    assert backend.available() is False

