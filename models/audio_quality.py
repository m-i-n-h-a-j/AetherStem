from pydantic import BaseModel
from enum import Enum

class QualityEstimate(str, Enum):
    LOSSLESS = "lossless"
    PROBABLE_320 = "probable 320kbps"
    PROBABLE_192 = "probable 192kbps"
    PROBABLE_128 = "probable 128kbps"
    UNKNOWN = "unknown"

class LossyDetectionResult(BaseModel):
    estimate: QualityEstimate
    confidence: float
    detected_cutoff_hz: float
    is_transcoded: bool
    details: str
