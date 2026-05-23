from __future__ import annotations

from ai.compute.backend import BackendSelection
from ai.models.base import AudioModel, ModelCompatibilityError
from ai.models.registry import ModelRegistry, default_registry


class ModelManager:
    def __init__(self, registry: ModelRegistry | None = None) -> None:
        self.registry = registry or default_registry
        self._loaded: dict[str, AudioModel] = {}

    def get(self, name: str, selection: BackendSelection) -> AudioModel:
        compatibility = self.registry.compatibility(name, selection.backend, selection.device)
        if not compatibility.compatible:
            raise ModelCompatibilityError(compatibility.reason or "Incompatible model/backend selection")
        if name not in self._loaded:
            self._loaded[name] = self.registry.create(name)
        return self._loaded[name]

