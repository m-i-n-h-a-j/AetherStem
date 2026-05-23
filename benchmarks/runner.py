from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


class BenchmarkRunner:
    def __init__(self, output_dir: Path | str = "benchmarks") -> None:
        self.output_dir = Path(output_dir)

    def run(self, input_path: Path, callable_obj) -> dict[str, Any]:
        started = time.perf_counter()
        result = callable_obj()
        runtime_ms = (time.perf_counter() - started) * 1000
        audio_seconds = _audio_seconds(result)
        report = {
            "input": str(input_path),
            "runtime_ms": runtime_ms,
            "latency_ms": runtime_ms,
            "throughput_audio_seconds_per_second": audio_seconds / (runtime_ms / 1000) if runtime_ms > 0 and audio_seconds else None,
            "memory": {},
            "backend": _stage_value(result, "backend"),
            "provider": _stage_value(result, "provider"),
            "chunk_scheduler": _chunk_scheduler_metrics(result),
            "result": result,
        }
        self.output_dir.mkdir(parents=True, exist_ok=True)
        report_path = self.output_dir / f"{input_path.stem}_benchmark.json"
        report_path.write_text(json.dumps(report, indent=2, default=str))
        report["report"] = str(report_path)
        return report


def _audio_seconds(result: Any) -> float | None:
    if isinstance(result, dict) and "audio" in result and "sample_rate" in result:
        audio = result["audio"]
        sample_rate = result["sample_rate"]
        try:
            return float(audio.shape[-1] / sample_rate)
        except Exception:
            return None
    return None


def _stage_value(result: Any, key: str) -> Any:
    if not isinstance(result, dict):
        return None
    if key in result:
        return result[key]
    return result.get("stages", {}).get("separate", {}).get("diagnostics", {}).get(key)


def _chunk_scheduler_metrics(result: Any) -> dict[str, Any]:
    if not isinstance(result, dict):
        return {}
    diagnostics = result.get("stages", {}).get("separate", {}).get("diagnostics", {})
    return {
        "chunk_size": diagnostics.get("chunk_size"),
        "overlap": diagnostics.get("overlap"),
        "hop_size": diagnostics.get("hop_size"),
        "batch_size": diagnostics.get("batch_size"),
        "chunks": diagnostics.get("chunks"),
        "estimated_memory_mb": diagnostics.get("estimated_memory_mb"),
    }
