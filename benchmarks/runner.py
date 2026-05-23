from __future__ import annotations

import json
import time
from pathlib import Path


class BenchmarkRunner:
    def __init__(self, output_dir: Path | str = "benchmarks") -> None:
        self.output_dir = Path(output_dir)

    def run(self, input_path: Path, callable_obj) -> dict:
        started = time.perf_counter()
        result = callable_obj()
        runtime_ms = (time.perf_counter() - started) * 1000
        report = {
            "input": str(input_path),
            "runtime_ms": runtime_ms,
            "latency_ms": runtime_ms,
            "memory": {},
            "quality": {},
            "result": result,
        }
        self.output_dir.mkdir(parents=True, exist_ok=True)
        report_path = self.output_dir / f"{input_path.stem}_benchmark.json"
        report_path.write_text(json.dumps(report, indent=2, default=str))
        report["report"] = str(report_path)
        return report

