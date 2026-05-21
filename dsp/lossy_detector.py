from models.audio_quality import LossyDetectionResult, QualityEstimate
from .spectrum import analyze_spectrum
import numpy as np

def detect_lossy(signal: np.ndarray, sample_rate: int) -> LossyDetectionResult:
    """
    Heuristic-based lossy source detection.
    Analyzes the high-frequency content to estimate if the source was originally lossy.
    """
    spec_analysis = analyze_spectrum(signal, sample_rate)
    cutoff = spec_analysis.hf_cutoff_hz
    
    estimate = QualityEstimate.UNKNOWN
    confidence = 0.5
    is_transcoded = False
    details = ""

    # Heuristics based on common encoder cutoffs
    if cutoff < 15500:
        estimate = QualityEstimate.PROBABLE_128
        confidence = 0.9
        is_transcoded = True
        details = f"Abrupt HF cutoff at {cutoff/1000:.1f}kHz (typical for 128kbps MP3)."
    elif cutoff < 17500:
        estimate = QualityEstimate.PROBABLE_192
        confidence = 0.8
        is_transcoded = True
        details = f"Abrupt HF cutoff at {cutoff/1000:.1f}kHz (typical for 192kbps MP3)."
    elif cutoff < 19500:
        estimate = QualityEstimate.PROBABLE_320
        confidence = 0.7
        is_transcoded = True
        details = f"Abrupt HF cutoff at {cutoff/1000:.1f}kHz (typical for 320kbps MP3/AAC)."
    elif cutoff >= 20000:
        estimate = QualityEstimate.LOSSLESS
        confidence = 0.8
        is_transcoded = False
        details = f"Full frequency spectrum preserved up to {cutoff/1000:.1f}kHz."
    
    return LossyDetectionResult(
        estimate=estimate,
        confidence=confidence,
        detected_cutoff_hz=cutoff,
        is_transcoded=is_transcoded,
        details=details
    )
