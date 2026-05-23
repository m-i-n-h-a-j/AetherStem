from __future__ import annotations

from pathlib import Path

from ai.backends.registry import default_backend_registry


def troubleshooting_report(config) -> dict:
    backend_diag = default_backend_registry.diagnostics()
    issues = []
    if not backend_diag.get("onnx", {}).get("available"):
        issues.append({
            "issue": "onnxruntime unavailable",
            "recommendation": "Install the runtime-cpu optional extra to enable ONNX CPU execution.",
        })
    if config.ai.model_path and not Path(config.ai.model_path).exists():
        issues.append({"issue": "configured model path missing", "recommendation": f"Check ai.model_path: {config.ai.model_path}"})
    if not config.ai.model_path:
        issues.append({"issue": "no ONNX model path configured", "recommendation": "Set ai.model_path or add a registry manifest asset for real model execution."})
    return {"backends": backend_diag, "issues": issues}
