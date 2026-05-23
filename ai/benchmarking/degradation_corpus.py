from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from validation.degradation import DegradationProfile, apply_degradation
from validation.synthetic_audio import SyntheticAudioFixture, generate_synthetic_suite


@dataclass(frozen=True)
class BenchmarkCase:
    fixture: SyntheticAudioFixture
    degradation: DegradationProfile
    degraded_samples: np.ndarray


class DegradationCorpus:
    def build(self, sample_rate: int = 48000, duration_seconds: float = 0.25) -> list[BenchmarkCase]:
        profiles = [
            DegradationProfile("lowpass", 0.7),
            DegradationProfile("clipping", 0.6),
            DegradationProfile("bitcrush", 0.5),
            DegradationProfile("transient_smear", 0.4),
        ]
        cases: list[BenchmarkCase] = []
        for fixture in generate_synthetic_suite(sample_rate, duration_seconds):
            for profile in profiles:
                cases.append(BenchmarkCase(fixture, profile, apply_degradation(fixture.samples, fixture.sample_rate, profile)))
        return cases
