import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from utils.logger import logger

@dataclass
class AudioConfig:
    sample_rate: int
    channels: int
    bit_depth: int
    format: str

@dataclass
class PipelineConfig:
    chunk_size: int
    overlap_ratio: float
    hop_length: int
    backend: str = "auto"
    device: str = "auto"
    fallback_to_cpu: bool = True

@dataclass
class AIConfig:
    models: Dict[str, str] = field(default_factory=dict)
    validation_thresholds: Dict[str, Any] = field(default_factory=dict)
    denoise_strength: float = 0.5
    enhancement_intensity: float = 0.5
    provider: str = "auto"
    precision: str = "fp32"
    low_memory: bool = False
    model_path: Optional[str] = None
    manifest_dirs: list[str] = field(default_factory=lambda: ["ai/models/registry/manifests"])
    model_cache_dir: str = "cache/models"
    runtime_profile: str = "auto"
    telemetry_enabled: bool = False
    profiling_enabled: bool = False

@dataclass
class PathConfig:
    temp_dir: str
    output_dir: str
    logs_dir: str
    exports_dir: str = "exports"
    benchmarks_dir: str = "benchmarks"

@dataclass
class AppConfig:
    audio: AudioConfig
    pipeline: PipelineConfig
    ai: AIConfig
    paths: PathConfig
    metadata: Dict[str, Any]

def load_config(config_path: Optional[Path] = None) -> AppConfig:
    """
    Loads and validates the application configuration from a YAML file.
    """
    if config_path is None:
        config_path = Path("configs/default.yaml")
    
    if not config_path.exists():
        logger.error(f"Configuration file not found at: {config_path}")
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    try:
        with open(config_path, "r") as f:
            data = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to parse YAML configuration: {e}")
        raise

    # Validation and object creation
    try:
        audio = AudioConfig(**data["audio"])
        pipeline = PipelineConfig(**data["pipeline"])
        ai = AIConfig(**data.get("ai", {}))
        paths = PathConfig(**data["paths"])
        metadata = data["metadata"]

        # Basic range validation
        if audio.sample_rate <= 0:
            raise ValueError("sample_rate must be positive")
        if pipeline.overlap_ratio < 0 or pipeline.overlap_ratio >= 1:
            raise ValueError("overlap_ratio must be between 0 and 1")

        config = AppConfig(
            audio=audio,
            pipeline=pipeline,
            ai=ai,
            paths=paths,
            metadata=metadata
        )
        logger.info(f"Configuration loaded successfully from {config_path}")
        return config
    except KeyError as e:
        logger.error(f"Missing required configuration parameter: {e}")
        raise
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        raise

# Singleton-like access for convenience
try:
    config = load_config()
except Exception:
    # If loading fails during import, we might want to handle it or just let it fail
    # For now, we'll let it fail if the default config is missing or invalid
    raise
