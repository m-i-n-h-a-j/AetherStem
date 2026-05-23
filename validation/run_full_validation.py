from __future__ import annotations

import argparse
import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path
from time import perf_counter
from typing import Any

import numpy as np

from validation.golden import GoldenReference, compare_golden_reference
from validation.metrics import compare_audio
from validation.reporting import CheckStatus, ValidationCheck, ValidationReport
from validation.static_checks import validate_config_schema, validate_import_graph
from validation.synthetic_audio import generate_synthetic_suite


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the AetherStem validation laboratory checks.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "reports" / "validation")
    parser.add_argument("--quick", action="store_true", help="Skip optional heavyweight stages.")
    parser.add_argument("--strict-static", action="store_true", help="Fail on ruff, mypy, and pyright findings.")
    args = parser.parse_args(argv)

    report = ValidationReport()
    _run_static_validation(report, strict=args.strict_static)
    _run_unit_tests(report)
    _run_dsp_verification(report)
    _run_golden_reference_checks(report)
    _record_deferred_enterprise_tiers(report, quick=args.quick)

    json_path = report.write_json(args.output_dir / "validation_report.json")
    html_path = report.write_html(args.output_dir / "validation_report.html")
    print(f"Validation JSON: {json_path}")
    print(f"Validation HTML: {html_path}")
    print(f"Validation summary: {report.summary()}")
    return 0 if report.passed else 1


def _run_static_validation(report: ValidationReport, strict: bool) -> None:
    _timed(report, "tier1-static", "config-schema", lambda: _assert_no_errors(validate_config_schema(ROOT / "configs" / "default.yaml")))
    _timed(
        report,
        "tier1-static",
        "import-graph",
        lambda: _assert_no_errors(validate_import_graph(_project_python_files())),
    )
    for module in ("ruff", "mypy", "pyright"):
        if not _tool_available(module):
            report.add(ValidationCheck("tier1-static", module, "skipped", {"reason": "tool not installed"}))
            continue
        command = _static_command(module)
        _timed(
            report,
            "tier1-static",
            module,
            lambda command=command: _run_command(command),
            failure_status="failed" if strict else "skipped",
            failure_details={"reason": "advisory static check failed; pass --strict-static to make this blocking"},
        )


def _run_unit_tests(report: ValidationReport) -> None:
    _timed(report, "tier2-unit", "pytest", lambda: _run_command([sys.executable, "-m", "pytest", "tests"]))


def _run_dsp_verification(report: ValidationReport) -> None:
    def check() -> None:
        for fixture in generate_synthetic_suite(duration_seconds=0.25):
            samples = fixture.samples
            restored = np.fft.irfft(np.fft.rfft(samples), n=samples.shape[-1]).astype(np.float32)
            result = compare_audio(samples, restored, fixture.sample_rate)
            if not result["passed"]:
                raise AssertionError({fixture.name: result["failures"]})

    _timed(report, "tier3-dsp", "fft-roundtrip-synthetic-suite", check)


def _run_golden_reference_checks(report: ValidationReport) -> None:
    def check() -> None:
        for fixture in generate_synthetic_suite(duration_seconds=0.25):
            reference = GoldenReference.from_samples(fixture.name, fixture.samples, fixture.sample_rate)
            result = compare_golden_reference(reference, fixture.samples.copy())
            if not result["passed"]:
                raise AssertionError({fixture.name: result["failures"]})

    _timed(report, "tier4-golden", "synthetic-golden-self-check", check)


def _record_deferred_enterprise_tiers(report: ValidationReport, quick: bool) -> None:
    details = {"reason": "requires dedicated hardware corpus or nightly budget", "quick": quick}
    for tier in (
        "tier5-pipeline-regression",
        "tier6-hardware-scalability",
        "tier7-memory-safety",
        "tier8-temporal-consistency",
        "tier9-perceptual-validation",
        "tier10-fuzz",
        "tier11-long-duration",
        "tier12-backend-equivalence",
        "tier13-cli-contract",
        "tier14-report-contract",
        "tier15-streaming",
    ):
        report.add(ValidationCheck(tier, "enterprise-suite", "skipped", details))


def _timed(
    report: ValidationReport,
    tier: str,
    name: str,
    func,
    failure_status: CheckStatus = "failed",
    failure_details: dict[str, Any] | None = None,
) -> None:
    started = perf_counter()
    try:
        func()
        status: CheckStatus = "passed"
        details: dict[str, Any] = {}
    except Exception as exc:
        status = failure_status
        details = {"error": str(exc), **(failure_details or {})}
    report.add(ValidationCheck(tier, name, status, details, (perf_counter() - started) * 1000))


def _run_command(command: list[str]) -> None:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        raise AssertionError({"command": command, "stdout": completed.stdout[-4000:], "stderr": completed.stderr[-4000:]})


def _static_command(module: str) -> list[str]:
    if module == "ruff":
        return [sys.executable, "-m", module, "check", "."]
    if module == "mypy":
        return [sys.executable, "-m", module, "ai", "audio_io", "benchmarks", "cli", "dsp", "models", "pipeline", "utils", "validation"]
    return [sys.executable, "-m", module]


def _tool_available(module: str) -> bool:
    return importlib.util.find_spec(module) is not None or shutil.which(module) is not None


def _assert_no_errors(errors: list[str]) -> None:
    if errors:
        raise AssertionError(errors)


def _project_python_files() -> list[Path]:
    roots = ["ai", "audio_io", "benchmarks", "cli", "dsp", "models", "pipeline", "utils", "validation"]
    return [path for root in roots for path in (ROOT / root).rglob("*.py")]


if __name__ == "__main__":
    raise SystemExit(main())
