import numpy as np
from dsp.loudness import analyze_loudness
from dsp.spectrum import analyze_spectrum
from dsp.stereo import analyze_stereo
from dsp.clipping import count_clipping
from dsp.noise_floor import estimate_noise_floor, estimate_dynamic_range
from dsp.lossy_detector import detect_lossy
from models.audio_analysis import AudioAnalysis
from models.audio_quality import LossyDetectionResult

class AnalyzeStage:
    def execute(self, signal: np.ndarray, sample_rate: int) -> tuple[AudioAnalysis, LossyDetectionResult]:
        loudness = analyze_loudness(signal, sample_rate)
        spectrum = analyze_spectrum(signal, sample_rate)
        stereo = analyze_stereo(signal)
        clipping = count_clipping(signal)
        noise_floor = estimate_noise_floor(signal)
        dynamic_range = estimate_dynamic_range(signal)
        
        quality = detect_lossy(signal, sample_rate)
        
        analysis = AudioAnalysis(
            loudness=loudness,
            spectrum=spectrum,
            stereo=stereo,
            clipping_count=clipping,
            noise_floor_db=noise_floor,
            dynamic_range_dr=dynamic_range
        )
        
        return analysis, quality
