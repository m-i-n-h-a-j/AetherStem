from __future__ import annotations

import json
from typing import Any

from cli.help.registry import HelpRegistry, default_help_registry
from cli.help.workflows import workflow_metadata


def agent_metadata(registry: HelpRegistry | None = None) -> dict[str, Any]:
    registry = registry or default_help_registry
    return {
        "schema": "aetherstem.cli.ai-metadata.v1",
        "project": "AetherStem",
        "commands": [command.as_dict() for command in registry.all()],
        "workflows": workflow_metadata(),
        "conventions": {
            "exports": "exports/",
            "reports": "reports/",
            "runtime_manifests": "ai/models/registry/manifests/",
            "model_cache": "cache/models/",
            "config": "configs/default.yaml",
        },
    }


def agent_metadata_json(registry: HelpRegistry | None = None) -> str:
    return json.dumps(agent_metadata(registry), indent=2, sort_keys=True)

