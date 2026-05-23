from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any

import numpy as np

from validation.metrics import compare_audio


@dataclass(frozen=True)
class GoldenReference:
    name: str
    samples: np.ndarray
    sample_rate: int
    checksum: str
    thresholds: dict[str, float]

    @classmethod
    def from_samples(
        cls,
        name: str,
        samples: np.ndarray,
        sample_rate: int,
        thresholds: dict[str, float] | None = None,
    ) -> "GoldenReference":
        array = np.asarray(samples, dtype=np.float32)
        return cls(
            name=name,
            samples=array,
            sample_rate=sample_rate,
            checksum=checksum_samples(array),
            thresholds=thresholds or {},
        )


def compare_golden_reference(reference: GoldenReference, candidate: np.ndarray) -> dict[str, Any]:
    result = compare_audio(reference.samples, candidate, reference.sample_rate, reference.thresholds)
    result["reference_name"] = reference.name
    result["reference_checksum"] = reference.checksum
    result["candidate_checksum"] = checksum_samples(np.asarray(candidate, dtype=np.float32))
    return result


def checksum_samples(samples: np.ndarray) -> str:
    return hashlib.sha256(np.ascontiguousarray(samples).tobytes()).hexdigest()
