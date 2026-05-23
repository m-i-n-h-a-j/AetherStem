from __future__ import annotations

import json
from pathlib import Path

import yaml

from ai.models.registry.metadata import ModelManifest
from ai.models.registry.validation import manifest_from_dict


class ManifestDiscovery:
    def __init__(self, roots: list[Path] | None = None) -> None:
        self.roots = roots or [Path("models/registry"), Path("ai/models/registry/manifests")]

    def discover(self) -> tuple[list[ModelManifest], list[dict]]:
        manifests: list[ModelManifest] = []
        errors: list[dict] = []
        for root in self.roots:
            if not root.exists():
                continue
            files = sorted([*root.glob("*.json"), *root.glob("*.yaml"), *root.glob("*.yml")])
            for path in files:
                try:
                    data = _load(path)
                    manifests.append(manifest_from_dict(data))
                except Exception as exc:
                    errors.append({"path": str(path), "error": str(exc)})
        return sorted(manifests, key=lambda item: (item.task, item.architecture, item.id, item.version)), errors


def _load(path: Path) -> dict:
    text = path.read_text()
    if path.suffix.lower() == ".json":
        return json.loads(text)
    return yaml.safe_load(text) or {}

