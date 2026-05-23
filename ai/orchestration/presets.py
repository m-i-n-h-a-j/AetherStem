from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class Preset(BaseModel):
    name: str
    workflow: str = "restore"
    force: list[str] = Field(default_factory=list)
    thresholds: dict[str, Any] = Field(default_factory=dict)
    config: dict[str, Any] = Field(default_factory=dict)


class PresetLoader:
    def __init__(self, preset_dir: Path | str = "presets") -> None:
        self.preset_dir = Path(preset_dir)

    def load(self, name: str) -> Preset:
        path = self.preset_dir / f"{name}.yaml"
        if not path.exists():
            raise FileNotFoundError(f"Unknown preset: {name}")
        data = yaml.safe_load(path.read_text()) or {}
        data.setdefault("name", name)
        return Preset(**data)

