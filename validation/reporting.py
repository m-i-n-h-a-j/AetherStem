from __future__ import annotations

from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
from time import time
from typing import Any, Literal


CheckStatus = Literal["passed", "failed", "skipped"]


@dataclass
class ValidationCheck:
    tier: str
    name: str
    status: CheckStatus
    details: dict[str, Any] = field(default_factory=dict)
    duration_ms: float = 0.0


@dataclass
class ValidationReport:
    version: str = "validation-framework-v1.0"
    started_at: float = field(default_factory=time)
    checks: list[ValidationCheck] = field(default_factory=list)

    def add(self, check: ValidationCheck) -> None:
        self.checks.append(check)

    @property
    def passed(self) -> bool:
        return all(check.status != "failed" for check in self.checks)

    def summary(self) -> dict[str, int]:
        counts = {"passed": 0, "failed": 0, "skipped": 0}
        for check in self.checks:
            counts[check.status] += 1
        return counts

    def to_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "started_at": self.started_at,
            "passed": self.passed,
            "summary": self.summary(),
            "checks": [asdict(check) for check in self.checks],
        }

    def write_json(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
        return path

    def write_html(self, path: Path) -> Path:
        path.parent.mkdir(parents=True, exist_ok=True)
        rows = "\n".join(
            f"<tr><td>{check.tier}</td><td>{check.name}</td><td>{check.status}</td><td>{check.duration_ms:.1f}</td></tr>"
            for check in self.checks
        )
        html = (
            "<!doctype html><html><head><meta charset=\"utf-8\"><title>AetherStem Validation</title>"
            "<style>body{font-family:Segoe UI,Arial,sans-serif;margin:32px}"
            "table{border-collapse:collapse;width:100%}td,th{border:1px solid #ccc;padding:6px}"
            "</style></head><body><h1>AetherStem Validation Report</h1>"
            f"<p>Passed: {self.passed}</p><pre>{json.dumps(self.summary(), indent=2)}</pre>"
            f"<table><thead><tr><th>Tier</th><th>Name</th><th>Status</th><th>ms</th></tr></thead><tbody>{rows}</tbody></table>"
            "</body></html>"
        )
        path.write_text(html, encoding="utf-8")
        return path


def validate_report_contract(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in ("version", "started_at", "passed", "summary", "checks"):
        if key not in payload:
            errors.append(f"missing required field: {key}")
    if "checks" in payload and not isinstance(payload["checks"], list):
        errors.append("checks must be a list")
    for index, check in enumerate(payload.get("checks", [])):
        for key in ("tier", "name", "status", "details", "duration_ms"):
            if key not in check:
                errors.append(f"checks[{index}] missing required field: {key}")
        if check.get("status") not in {"passed", "failed", "skipped"}:
            errors.append(f"checks[{index}] has invalid status: {check.get('status')}")
    return errors
