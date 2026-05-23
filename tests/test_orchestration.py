from ai.orchestration.decision_engine import DecisionEngine
from models.audio_analysis import AudioAnalysis, LoudnessAnalysis, SpectrumAnalysis, StereoAnalysis


def _analysis(noise_floor_db=-80.0, clipping_count=0):
    return AudioAnalysis(
        loudness=LoudnessAnalysis(
            integrated_lufs=-18.0,
            short_term_max=-12.0,
            momentary_max=-10.0,
            lra=5.0,
            true_peak_db=-1.0,
        ),
        spectrum=SpectrumAnalysis(
            spectral_centroid_avg=1000.0,
            spectral_rolloff_avg=8000.0,
            spectral_bandwidth_avg=2000.0,
            hf_cutoff_hz=18000.0,
        ),
        stereo=StereoAnalysis(
            stereo_width=1.0,
            mid_energy=0.5,
            side_energy=0.5,
            phase_correlation=0.9,
            is_mono=False,
        ),
        clipping_count=clipping_count,
        noise_floor_db=noise_floor_db,
        dynamic_range_dr=10.0,
    )


def test_clean_input_skips_unneeded_processing():
    plan = DecisionEngine().plan(_analysis())

    assert not plan.enabled("denoise")
    assert not plan.enabled("declip")
    assert not plan.enabled("enhance")
    assert plan.enabled("validate")
    assert plan.enabled("export")


def test_noise_above_threshold_enables_denoise():
    plan = DecisionEngine().plan(_analysis(noise_floor_db=-40.0))

    assert plan.enabled("denoise")

