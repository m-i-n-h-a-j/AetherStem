import json

import numpy as np

from validation.degradation import DegradationProfile, apply_degradation
from validation.golden import GoldenReference, compare_golden_reference
from validation.matrix import default_validation_matrix
from validation.metrics import compare_audio, compute_audio_metrics
from validation.reporting import ValidationCheck, ValidationReport, validate_report_contract
from validation.synthetic_audio import generate_synthetic_suite


def test_synthetic_suite_is_deterministic():
    first = generate_synthetic_suite(duration_seconds=0.05)
    second = generate_synthetic_suite(duration_seconds=0.05)

    assert [item.name for item in first] == [item.name for item in second]
    assert [item.checksum for item in first] == [item.checksum for item in second]


def test_audio_metrics_and_golden_reference_detect_drift():
    fixture = generate_synthetic_suite(duration_seconds=0.05)[0]
    candidate = fixture.samples.copy()
    candidate[100:120] += 0.01
    reference = GoldenReference.from_samples(fixture.name, fixture.samples, fixture.sample_rate)

    metrics = compute_audio_metrics(fixture.samples, fixture.sample_rate)
    result = compare_golden_reference(reference, candidate)

    assert metrics.peak > 0.0
    assert not result["passed"]
    assert "waveform_rmse" in result["metrics"]


def test_degradation_profiles_change_audio_predictably():
    fixture = generate_synthetic_suite(duration_seconds=0.05)[0]
    degraded = apply_degradation(fixture.samples, fixture.sample_rate, DegradationProfile("bitcrush", 1.0))

    result = compare_audio(fixture.samples, degraded, fixture.sample_rate)

    assert degraded.dtype == np.float32
    assert result["metrics"]["waveform_rmse"] > 0.0


def test_validation_matrix_generates_combinations():
    matrix = default_validation_matrix(
        pipelines=("reconstruct",),
        backends=("numpy", "onnx"),
        precisions=("fp32",),
        qualities=("balanced",),
        devices=("cpu",),
        chunk_sizes=(1024,),
        streaming_modes=(False, True),
    )

    assert len(matrix) == 4
    assert matrix[0].id().startswith("reconstruct-")


def test_validation_report_contract(tmp_path):
    report = ValidationReport()
    report.add(ValidationCheck("tier1-static", "config", "passed", {"ok": True}, 1.0))
    path = report.write_json(tmp_path / "report.json")
    payload = json.loads(path.read_text(encoding="utf-8"))

    assert validate_report_contract(payload) == []
    assert payload["summary"]["passed"] == 1
