import hashlib
import json
from pathlib import Path
from typing import Optional, Any
from models.pipeline_result import PipelineResult
from utils.logger import logger

class AnalysisCache:
    def __init__(self, cache_dir: Path = Path("cache")):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_hash(self, file_path: Path) -> str:
        """Calculates SHA256 of the file content."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def get(self, file_path: Path) -> Optional[PipelineResult]:
        """Retrieves cached result if it exists."""
        file_hash = self._get_hash(file_path)
        cache_file = self.cache_dir / f"{file_hash}.json"
        
        if cache_file.exists():
            logger.info(f"Cache hit for {file_path.name}")
            with open(cache_file, "r") as f:
                return PipelineResult.model_validate_json(f.read())
        return None

    def set(self, file_path: Path, result: PipelineResult):
        """Stores result in cache."""
        file_hash = self._get_hash(file_path)
        cache_file = self.cache_dir / f"{file_hash}.json"
        
        with open(cache_file, "w") as f:
            f.write(result.model_dump_json())
        logger.info(f"Cached result for {file_path.name}")
