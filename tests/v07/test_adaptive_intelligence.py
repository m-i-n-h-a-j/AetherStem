import numpy as np

from ai.benchmarking.degradation_corpus import DegradationCorpus
from ai.reconstruction.intelligence import ArtifactIntelligenceEngine, ConfidenceGate, ModulePolicy, RegionClassifier
from ai.reconstruction.perceptual import PsychoacousticEngine
from ai.reconstruction.temporal import TemporalStabilityEngine
from ai.runtime.audio_buffer import AudioBuffer
from ai.runtime.graph import RuntimeGraphDescriptor, RuntimeNodeDescriptor
from ai.runtime.memory import AdaptiveMemoryPlanner
from ai.runtime.profiling.hardware import HardwareTier
from ai.runtime.quality import QualityProfile, QualityScaler
from ai.runtime.scheduling import AdaptiveScheduler


def _audio() -> AudioBuffer:
    sample_rate = 48000
    t = np.arange(sample_rate // 4, dtype=np.float64) / sample_rate
    left = 0.4 * np.sin(2 * np.pi * 440 * t)
    right = 0.4 * np.sin(2 * np.pi * 440 * t + np.pi / 4)
    impulse = np.zeros_like(left)
    impulse[len(impulse) // 2] = 0.8
    return AudioBuffer(np.vstack([left + impulse, right]), sample_rate=sample_rate, layout="channels_first")


def test_artifact_intelligence_is_deterministic():
    audio = _audio()
    engine = ArtifactIntelligenceEngine()

    first, first_heatmap = engine.analyze(audio)
    second, second_heatmap = engine.analyze(audio)

    assert [item.to_dict() for item in first] == [item.to_dict() for item in second]
    assert first_heatmap.summary() == second_heatmap.summary()
    assert set(first_heatmap.summary()) == {
        "spectral_artifact_mean",
        "temporal_confidence_mean",
        "reconstruction_danger_mean",
        "stereo_instability_mean",
        "transient_degradation_mean",
    }


def test_confidence_gate_clamps_low_confidence_regions():
    gate = ConfidenceGate()
    policy = ModulePolicy("harmonic_regeneration", minimum_confidence=0.65, safe_min=0.1, safe_max=0.8)

    assert gate.clamp(policy, confidence=0.2, requested_aggressiveness=1.0) == 0.0
    assert 0.0 < gate.clamp(policy, confidence=0.9, requested_aggressiveness=1.0, danger=0.4) <= 0.8


def test_region_temporal_and_perceptual_reports_are_bounded():
    audio = _audio()

    region_map = RegionClassifier().classify(audio)
    temporal = TemporalStabilityEngine().analyze(audio)
    perceptual = PsychoacousticEngine().analyze(audio)

    assert region_map.regions
    assert 0.0 <= temporal.stability_score <= 1.0
    assert 0.0 <= perceptual.perceptual_score <= 1.0


def test_quality_scaling_scheduler_and_memory_planner_clamp_legacy_hardware():
    quality = QualityScaler().plan(QualityProfile.FORENSIC_EXTREME, hardware_tier=HardwareTier.LEGACY, available_memory_mb=1024)
    schedule = AdaptiveScheduler().plan(quality, sample_rate=48000, recommended_concurrency=4)
    memory = AdaptiveMemoryPlanner().plan(channels=2, chunk_size=schedule.chunk_size, available_mb=1024)

    assert quality.clamped is True
    assert schedule.streaming is True
    assert schedule.concurrency == 1
    assert memory.batch_size >= 1


def test_runtime_graph_descriptor_fingerprint_is_stable():
    graph = RuntimeGraphDescriptor(
        (
            RuntimeNodeDescriptor("spectral_repair", cpu_cost=0.4, vram_cost_mb=128, latency_ms=20, parallelizable=True),
            RuntimeNodeDescriptor("mastering", cpu_cost=0.2, vram_cost_mb=32, latency_ms=5, dependencies=("spectral_repair",)),
        )
    )

    assert graph.fingerprint() == graph.fingerprint()
    assert graph.total_vram_mb() == 160
    assert graph.deterministic() is True


def test_degradation_corpus_builds_reproducible_cases():
    cases = DegradationCorpus().build(duration_seconds=0.05)

    assert cases
    assert cases[0].degraded_samples.shape == cases[0].fixture.samples.shape
