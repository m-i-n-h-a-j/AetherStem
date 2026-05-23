from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import numpy as np


class RuntimeProviderBenchmark:
    def __init__(self, output_dir: Path | str = "benchmarks") -> None:
        self.output_dir = Path(output_dir)

    def run(self, iterations: int = 20, warmup: int = 5) -> dict[str, Any]:
        import onnx
        import onnxruntime as ort
        from onnx import TensorProto, helper

        self.output_dir.mkdir(parents=True, exist_ok=True)
        model_path = self.output_dir / "runtime_provider_benchmark.onnx"
        _write_matmul_model(model_path, helper, TensorProto, onnx)

        rng = np.random.default_rng(1337)
        sample = rng.normal(size=(256, 256)).astype(np.float32)
        available = ort.get_available_providers()
        targets = [
            ("cpu", "CPUExecutionProvider"),
            ("cuda", "CUDAExecutionProvider"),
            ("tensorrt", "TensorrtExecutionProvider"),
        ]
        results = []
        for name, provider in targets:
            if provider not in available:
                results.append({"name": name, "provider": provider, "available": False, "status": "unavailable"})
                continue
            results.append(_benchmark_provider(model_path, sample, name, provider, iterations, warmup))

        report = {
            "available_providers": available,
            "provider_priority": ["TensorrtExecutionProvider", "CUDAExecutionProvider", "CPUExecutionProvider"],
            "iterations": iterations,
            "warmup": warmup,
            "results": results,
        }
        report_path = self.output_dir / "runtime_provider_benchmark.json"
        report_path.write_text(json.dumps(report, indent=2, default=str))
        report["report"] = str(report_path)
        return report


def _write_matmul_model(model_path: Path, helper, tensor_proto, onnx_module) -> None:
    if model_path.exists():
        return
    rng = np.random.default_rng(2026)
    weights = rng.normal(size=(256, 256)).astype(np.float32)
    graph = helper.make_graph(
        nodes=[helper.make_node("MatMul", ["input", "weights"], ["output"])],
        name="runtime_provider_benchmark",
        inputs=[helper.make_tensor_value_info("input", tensor_proto.FLOAT, [256, 256])],
        outputs=[helper.make_tensor_value_info("output", tensor_proto.FLOAT, [256, 256])],
        initializer=[helper.make_tensor("weights", tensor_proto.FLOAT, weights.shape, weights.flatten().tolist())],
    )
    model = helper.make_model(graph, producer_name="aetherstem-runtime-benchmark", opset_imports=[helper.make_operatorsetid("", 13)])
    model.ir_version = 10
    onnx_module.save(model, model_path)


def _benchmark_provider(
    model_path: Path,
    sample: np.ndarray,
    name: str,
    provider: str,
    iterations: int,
    warmup: int,
) -> dict[str, Any]:
    try:
        session = _session(model_path, provider)
        input_name = session.get_inputs()[0].name
        for _ in range(warmup):
            session.run(None, {input_name: sample})
        started = time.perf_counter()
        for _ in range(iterations):
            session.run(None, {input_name: sample})
        elapsed_ms = (time.perf_counter() - started) * 1000
        actual = session.get_providers()[0] if session.get_providers() else provider
        status = "ok" if actual == provider else "fallback"
        return {
            "name": name,
            "provider": provider,
            "actual_provider": actual,
            "available": True,
            "status": status,
            "warning": None if status == "ok" else f"Requested {provider}, but ONNX Runtime initialized {actual}.",
            "total_ms": elapsed_ms,
            "mean_ms": elapsed_ms / iterations if iterations else None,
        }
    except Exception as exc:
        return {
            "name": name,
            "provider": provider,
            "available": True,
            "status": "failed",
            "error": str(exc),
        }


def _session(model_path: Path, provider: str):
    import onnxruntime as ort

    options = ort.SessionOptions()
    options.log_severity_level = 3
    return ort.InferenceSession(str(model_path), sess_options=options, providers=[provider])
