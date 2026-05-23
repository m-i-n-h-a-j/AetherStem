from __future__ import annotations

from ai.models.registry.cache import ModelCache
from ai.models.registry.metadata import ModelManifest


class ModelLifecycleManager:
    def __init__(self, cache: ModelCache | None = None) -> None:
        self.cache = cache or ModelCache()

    def status(self, manifest: ModelManifest) -> dict:
        cache_status = self.cache.validate(manifest)
        downloadable = bool(manifest.asset and manifest.asset.url) or bool(manifest.source_url)
        return {
            "id": manifest.id,
            "version": manifest.version,
            "cache": cache_status,
            "downloadable": downloadable,
            "source_url": manifest.source_url or (manifest.asset.url if manifest.asset else None),
        }

