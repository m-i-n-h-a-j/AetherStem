from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class SourceProfile:
    likely_source: str
    estimated_bitrate_kbps: int | None
    lossy_probability: float
    transcode_probability: float
    confidence: float


@dataclass(frozen=True)
class ArtifactProfile:
    spectral_cutoff_hz: float
    codec_ringing: float
    transient_smear: float
    stereo_collapse: float
    clipping_detected: bool
    limiter_detected: bool
    phase_corruption: float
    spectral_sparsity: float
    temporal_inconsistency: float
    detected_artifacts: tuple[str, ...] = ()


@dataclass(frozen=True)
class SpectralFingerprint:
    centroid_hz: float
    rolloff_hz: float
    bandwidth_hz: float
    ceiling_hz: float
    high_frequency_energy_ratio: float
    spectral_flatness: float


@dataclass(frozen=True)
class RestorationFeasibility:
    potential: str
    score: float
    recommended_stages: tuple[str, ...]
    caveats: tuple[str, ...] = ()


@dataclass(frozen=True)
class RestorationConfidence:
    confidence: float
    uncertainty: float
    rationale: tuple[str, ...] = ()


@dataclass(frozen=True)
class ForensicReport:
    source: SourceProfile
    artifacts: ArtifactProfile
    spectral: SpectralFingerprint
    feasibility: RestorationFeasibility
    confidence: RestorationConfidence
    philosophy: str = "AetherStem performs plausible reconstruction and remastering, not true lossless recovery."
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

