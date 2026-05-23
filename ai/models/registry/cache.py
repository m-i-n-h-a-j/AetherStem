from __future__ import annotations

import hashlib
from pathlib import Path

from ai.models.registry.metadata import ModelManifest


class ModelCache:
    def __init__(self, root: Path | str = "cache/models") -> None:
        self.root = Path(root)

    def path_for(self, manifest: ModelManifest) -> Path | None:
        if manifest.asset and manifest.asset.path:
            return Path(manifest.asset.path)
        if manifest.asset and manifest.asset.cache_key:
            return self.root / manifest.asset.cache_key
        return None

    def validate(self, manifest: ModelManifest) -> dict:
        path = self.path_for(manifest)
        expected = (manifest.asset.sha256 if manifest.asset and manifest.asset.sha256 else manifest.sha256).lower()
        if path is None:
            return {"available": False, "reason": "manifest has no local asset path"}
        if not path.exists():
            return {"available": False, "path": str(path), "reason": "asset is missing"}
        if expected:
            actual = sha256(path)
            if actual.lower() != expected:
                return {"available": False, "path": str(path), "reason": "checksum mismatch", "expected": expected, "actual": actual}
        return {"available": True, "path": str(path)}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()

