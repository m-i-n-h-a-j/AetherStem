from pydantic import BaseModel, Field
from typing import Optional

class AudioMetadata(BaseModel):
    """Basic audio file metadata."""
    filename: str
    format: str
    codec: str
    sample_rate: int
    channels: int
    bit_depth: int
    duration: float
    filesize_bytes: Optional[int] = None

    class Config:
        frozen = True  # Immutable
