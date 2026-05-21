from pydantic import BaseModel
from typing import Optional, Dict, Any
from .audio_metadata import AudioMetadata
from .audio_analysis import AudioAnalysis
from .audio_quality import LossyDetectionResult

class PipelineResult(BaseModel):
    metadata: AudioMetadata
    analysis: Optional[AudioAnalysis] = None
    quality: Optional[LossyDetectionResult] = None
    artifacts: Dict[str, str] = {}  # Paths to generated files (spectrograms, etc.)
    success: bool
    error: Optional[str] = None
