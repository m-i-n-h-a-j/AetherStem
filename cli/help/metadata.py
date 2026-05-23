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
            "benchmarks": "benchmarks/",
            "reports": "reports/",
            "runtime_manifests": "ai/models/registry/manifests/",
            "model_cache": "cache/models/",
            "config": "configs/default.yaml",
            "runtime_artifacts": "Generated exports, benchmark JSON, cache, reports, logs, output previews, and validation reports are runtime artifacts and are ignored except .gitkeep placeholders.",
            "validation_reports": "reports/validation/",
            "validation_spec": "openspec/changes/aetherstem-validation-framework-v1-0/",
            "v0_7_spec": "openspec/changes/aetherstem-core-v0-7-adaptive-intelligence/",
        },
    }


def agent_metadata_json(registry: HelpRegistry | None = None) -> str:
    return json.dumps(agent_metadata(registry), indent=2, sort_keys=True)
