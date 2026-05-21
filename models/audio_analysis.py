from pydantic import BaseModel
from typing import List, Dict, Optional

class LoudnessAnalysis(BaseModel):
    integrated_lufs: float
    short_term_max: float
    momentary_max: float
    lra: float
    true_peak_db: float

class SpectrumAnalysis(BaseModel):
    spectral_centroid_avg: float
    spectral_rolloff_avg: float
    spectral_bandwidth_avg: float
    hf_cutoff_hz: float
    average_spectrum: Optional[List[float]] = None

class StereoAnalysis(BaseModel):
    stereo_width: float
    mid_energy: float
    side_energy: float
    phase_correlation: float
    is_mono: bool

class AudioAnalysis(BaseModel):
    loudness: LoudnessAnalysis
    spectrum: SpectrumAnalysis
    stereo: StereoAnalysis
    clipping_count: int
    noise_floor_db: float
    dynamic_range_dr: float
