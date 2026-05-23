from __future__ import annotations

import numpy as np

from ai.reconstruction.analysis.profiles import (
    ArtifactProfile,
    ForensicReport,
    RestorationConfidence,
    RestorationFeasibility,
    SourceProfile,
    SpectralFingerprint,
)
from ai.runtime.audio_buffer import AudioBuffer


class ForensicAnalyzer:
    def analyze(self, audio: AudioBuffer) -> ForensicReport:
        samples = audio.as_channels_first().samples.astype(np.float64, copy=False)
        mono = np.mean(samples, axis=0)
        spectral = self._spectral_fingerprint(mono, audio.sample_rate)
        clipping = bool(np.any(np.abs(samples) >= 0.999))
        stereo_collapse = self._stereo_collapse(samples)
        transient_smear = self._transient_smear(mono)
        ringing = self._codec_ringing(mono)
        lossy_probability = self._lossy_probability(spectral, ringing, transient_smear)
        transcode_probability = min(1.0, lossy_probability * 0.65 + (0.25 if spectral.ceiling_hz < audio.sample_rate * 0.35 else 0.0))
        likely_source, bitrate = self._source_guess(spectral.ceiling_hz, lossy_probability, stereo_collapse)
        artifacts = self._artifact_profile(spectral, clipping, stereo_collapse, transient_smear, ringing, samples)
        feasibility = self._feasibility(artifacts, lossy_probability)
        confidence_value = float(np.clip(0.45 + lossy_probability * 0.35 + len(artifacts.detected_artifacts) * 0.03, 0.0, 0.95))
        confidence = RestorationConfidence(
            confidence=confidence_value,
            uncertainty=1.0 - confidence_value,
            rationale=(
                "spectral ceiling and artifact heuristics",
                "confidence is probabilistic and not proof of original source",
            ),
        )
        source = SourceProfile(likely_source, bitrate, lossy_probability, transcode_probability, confidence_value)
        return ForensicReport(source=source, artifacts=artifacts, spectral=spectral, feasibility=feasibility, confidence=confidence)

    def _spectral_fingerprint(self, mono: np.ndarray, sample_rate: int) -> SpectralFingerprint:
        if mono.size == 0:
            return SpectralFingerprint(0, 0, 0, 0, 0, 0)
        window = np.hanning(min(len(mono), 8192))
        segment = mono[: len(window)] * window
        spectrum = np.abs(np.fft.rfft(segment)) + 1e-12
        freqs = np.fft.rfftfreq(len(segment), 1 / sample_rate)
        total = float(np.sum(spectrum))
        centroid = float(np.sum(freqs * spectrum) / total)
        cumulative = np.cumsum(spectrum)
        rolloff = float(freqs[min(len(freqs) - 1, int(np.searchsorted(cumulative, total * 0.95)))])
        bandwidth = float(np.sqrt(np.sum(((freqs - centroid) ** 2) * spectrum) / total))
        threshold = np.max(spectrum) * 0.01
        active = freqs[spectrum >= threshold]
        ceiling = float(active[-1]) if active.size else 0.0
        hf_start = sample_rate * 0.35
        hf_energy = float(np.sum(spectrum[freqs >= hf_start]) / total)
        flatness = float(np.exp(np.mean(np.log(spectrum))) / np.mean(spectrum))
        return SpectralFingerprint(centroid, rolloff, bandwidth, ceiling, hf_energy, flatness)

    def _stereo_collapse(self, samples: np.ndarray) -> float:
        if samples.shape[0] < 2:
            return 1.0
        left, right = samples[0], samples[1]
        denom = np.sqrt(np.sum(left**2) * np.sum(right**2))
        corr = float(np.sum(left * right) / denom) if denom > 0 else 1.0
        return float(np.clip((corr - 0.65) / 0.35, 0.0, 1.0))

    def _transient_smear(self, mono: np.ndarray) -> float:
        diff = np.abs(np.diff(mono, prepend=mono[:1]))
        if diff.size == 0:
            return 0.0
        peak = np.percentile(diff, 99)
        median = np.median(diff) + 1e-9
        sharpness = peak / median
        return float(np.clip(1.0 - (sharpness / 40.0), 0.0, 1.0))

    def _codec_ringing(self, mono: np.ndarray) -> float:
        if mono.size < 4:
            return 0.0
        second = np.abs(np.diff(mono, n=2))
        return float(np.clip(np.percentile(second, 95) * 12.0, 0.0, 1.0))

    def _lossy_probability(self, spectral: SpectralFingerprint, ringing: float, smear: float) -> float:
        cutoff_score = 1.0 if spectral.ceiling_hz < 16500 else 0.5 if spectral.ceiling_hz < 19000 else 0.0
        hf_score = float(np.clip(1.0 - spectral.high_frequency_energy_ratio * 20.0, 0.0, 1.0))
        return float(np.clip(cutoff_score * 0.45 + hf_score * 0.25 + ringing * 0.15 + smear * 0.15, 0.0, 1.0))

    def _source_guess(self, ceiling: float, lossy_probability: float, stereo_collapse: float) -> tuple[str, int | None]:
        if lossy_probability > 0.75 and ceiling < 16500:
            return ("Likely 128kbps joint stereo MP3/AAC", 128 if stereo_collapse > 0.4 else 160)
        if lossy_probability > 0.55:
            return ("Likely lossy transcode", 192)
        return ("Likely high-quality or lossless source", None)

    def _artifact_profile(
        self,
        spectral: SpectralFingerprint,
        clipping: bool,
        stereo_collapse: float,
        transient_smear: float,
        ringing: float,
        samples: np.ndarray,
    ) -> ArtifactProfile:
        phase_corruption = float(np.clip(stereo_collapse * 0.5, 0.0, 1.0))
        sparsity = float(np.clip(1.0 - spectral.spectral_flatness, 0.0, 1.0))
        temporal = transient_smear
        artifacts = []
        if spectral.ceiling_hz < 18000:
            artifacts.append("spectral cutoff")
        if ringing > 0.35:
            artifacts.append("codec ringing")
        if transient_smear > 0.35:
            artifacts.append("transient softening")
        if stereo_collapse > 0.35:
            artifacts.append("stereo collapse")
        if clipping:
            artifacts.append("clipped transients")
        limiter = bool(np.percentile(np.abs(samples), 99.9) > 0.95 and not clipping)
        if limiter:
            artifacts.append("limiter flattening")
        return ArtifactProfile(
            spectral_cutoff_hz=spectral.ceiling_hz,
            codec_ringing=ringing,
            transient_smear=transient_smear,
            stereo_collapse=stereo_collapse,
            clipping_detected=clipping,
            limiter_detected=limiter,
            phase_corruption=phase_corruption,
            spectral_sparsity=sparsity,
            temporal_inconsistency=temporal,
            detected_artifacts=tuple(artifacts),
        )

    def _feasibility(self, artifacts: ArtifactProfile, lossy_probability: float) -> RestorationFeasibility:
        score = 0.35 + (0.25 if lossy_probability < 0.8 else 0.1)
        score += 0.1 if artifacts.clipping_detected else 0.0
        score += 0.1 if artifacts.spectral_cutoff_hz > 12000 else -0.05
        score = float(np.clip(score, 0.0, 1.0))
        potential = "High" if score >= 0.7 else "Moderate" if score >= 0.45 else "Limited"
        stages = []
        if artifacts.clipping_detected:
            stages.append("declip")
        if artifacts.spectral_cutoff_hz < 19000:
            stages.extend(["spectral_repair", "bandwidth_extension", "harmonic_regeneration"])
        if artifacts.transient_smear > 0.25:
            stages.append("transient_recovery")
        if artifacts.stereo_collapse > 0.25:
            stages.append("stereo_reconstruction")
        stages.extend(["psychoacoustic_optimization", "mastering"])
        return RestorationFeasibility(
            potential=potential,
            score=score,
            recommended_stages=tuple(dict.fromkeys(stages)),
            caveats=("Output is perceptual reconstruction, not original master recovery.",),
        )

