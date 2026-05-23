import json

from cli.help.metadata import agent_metadata_json
from cli.help.registry import default_help_registry
from cli.help.workflows import workflow_for


def test_help_registry_resolves_runtime_alias():
    command = default_help_registry.get("runtime")

    assert command is not None
    assert command.name == "runtime-diagnostics"


def test_agent_metadata_is_json_and_deterministic_shape():
    payload = json.loads(agent_metadata_json())

    assert payload["schema"] == "aetherstem.cli.ai-metadata.v1"
    assert "commands" in payload
    assert "workflows" in payload
    assert any(command["name"] == "separate" for command in payload["commands"])


def test_workflow_guidance_search():
    workflows = workflow_for("separate")

    assert workflows
    assert workflows[0]["name"] == "separate_stems"

