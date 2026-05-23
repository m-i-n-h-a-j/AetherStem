from __future__ import annotations

from ai.models.registry.metadata import ModelManifest


def compatibility_reasons(
    manifest: ModelManifest,
    task: str | None = None,
    backend: str | None = None,
    precision: str | None = None,
    sample_rate: int | None = None,
    channels: int | None = None,
    stems: list[str] | None = None,
) -> list[str]:
    reasons: list[str] = []
    if task and manifest.task != task:
        reasons.append(f"task mismatch: {manifest.task} != {task}")
    if backend and backend != "auto" and backend not in manifest.supported_backends:
        reasons.append(f"backend {backend} not in {manifest.supported_backends}")
    if precision and precision != "auto" and precision not in manifest.supported_precisions:
        reasons.append(f"precision {precision} not in {manifest.supported_precisions}")
    if sample_rate and manifest.sample_rate != sample_rate:
        reasons.append(f"sample_rate {manifest.sample_rate} != {sample_rate}")
    if channels and manifest.channels != channels:
        reasons.append(f"channels {manifest.channels} != {channels}")
    if stems:
        missing = [stem for stem in stems if stem not in manifest.stems]
        if missing:
            reasons.append(f"missing stems: {missing}")
    return reasons

