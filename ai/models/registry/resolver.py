from __future__ import annotations

from ai.models.registry.cache import ModelCache
from ai.models.registry.compatibility import compatibility_reasons
from ai.models.registry.metadata import ModelManifest, ResolvedModel


class ModelResolver:
    def __init__(self, manifests: list[ModelManifest], cache: ModelCache | None = None) -> None:
        self.manifests = sorted(manifests, key=lambda item: (item.task, item.architecture, item.id, item.version))
        self.cache = cache or ModelCache()

    def resolve(
        self,
        task: str,
        backend: str = "auto",
        device: str = "auto",
        precision: str = "fp32",
        sample_rate: int | None = None,
        channels: int | None = None,
        stems: list[str] | None = None,
        require_asset: bool = False,
    ) -> ResolvedModel:
        rejected = []
        for manifest in self.manifests:
            reasons = compatibility_reasons(manifest, task, backend, precision, sample_rate, channels, stems)
            if reasons:
                rejected.append({"id": manifest.id, "version": manifest.version, "reasons": reasons})
                continue
            cache_status = self.cache.validate(manifest)
            if require_asset and not cache_status.get("available"):
                rejected.append({"id": manifest.id, "version": manifest.version, "reasons": [str(cache_status)]})
                continue
            selected_backend = manifest.supported_backends[0] if backend == "auto" else backend
            selected_precision = manifest.supported_precisions[0] if precision == "auto" else precision
            return ResolvedModel(
                manifest=manifest,
                asset_path=self.cache.path_for(manifest),
                backend=selected_backend,
                device=device,
                precision=selected_precision,
                diagnostics={"cache": cache_status, "rejected": rejected},
            )
        raise LookupError(f"No compatible model found for task={task}; rejected={rejected}")

