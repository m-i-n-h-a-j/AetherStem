from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from ai.models.base import AudioModel
from ai.models.metadata import ModelCapabilities, ModelCompatibility, ModelMetadata


ModelFactory = Callable[[], AudioModel]


@dataclass(frozen=True)
class RegisteredModel:
    metadata: ModelMetadata
    factory: ModelFactory


class ModelRegistry:
    def __init__(self) -> None:
        self._models: dict[str, RegisteredModel] = {}

    def register(self, metadata: ModelMetadata, factory: ModelFactory) -> None:
        self._models[metadata.name] = RegisteredModel(metadata=metadata, factory=factory)

    def names(self) -> list[str]:
        return sorted(self._models)

    def metadata(self, name: str) -> ModelMetadata:
        return self._models[name].metadata

    def list(self) -> list[ModelMetadata]:
        return [entry.metadata for _, entry in sorted(self._models.items())]

    def find(self, capability: str | None = None, **flags: bool) -> list[ModelMetadata]:
        results = self.list()
        if capability:
            results = [item for item in results if item.capabilities.has(capability)]
        for key, expected in flags.items():
            results = [
                item for item in results
                if bool(getattr(item.capabilities, key, False)) is expected
            ]
        return results

    def create(self, name: str) -> AudioModel:
        if name not in self._models:
            raise KeyError(f"Unknown model: {name}")
        return self._models[name].factory()

    def compatibility(self, name: str, backend: str, device: str) -> ModelCompatibility:
        metadata = self.metadata(name)
        if backend not in metadata.requirements.backends:
            return ModelCompatibility(
                compatible=False,
                backend=backend,
                device=device,
                reason=f"Model requires one of {metadata.requirements.backends}",
            )
        if device not in metadata.requirements.devices and "any" not in metadata.requirements.devices:
            return ModelCompatibility(
                compatible=False,
                backend=backend,
                device=device,
                reason=f"Model requires one of {metadata.requirements.devices}",
            )
        return ModelCompatibility(compatible=True, backend=backend, device=device)


default_registry = ModelRegistry()


def _register_builtin_placeholders() -> None:
    from ai.models.demucs.adapter import DemucsPlaceholderModel
    from ai.models.denoise.adapter import DenoisePlaceholderModel
    from ai.models.enhancement.adapter import EnhancementPlaceholderModel
    from ai.models.mdx.adapter import MdxPlaceholderModel
    from ai.models.super_resolution.adapter import SuperResolutionPlaceholderModel

    for model_cls in (
        DemucsPlaceholderModel,
        DenoisePlaceholderModel,
        EnhancementPlaceholderModel,
        MdxPlaceholderModel,
        SuperResolutionPlaceholderModel,
    ):
        default_registry.register(model_cls.metadata, model_cls)


_register_builtin_placeholders()

