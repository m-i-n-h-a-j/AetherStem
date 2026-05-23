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
    assert any(command["name"] == "validation" for command in payload["commands"])
    assert any(command["name"] == "adaptive-intelligence" for command in payload["commands"])
    assert payload["conventions"]["validation_reports"] == "reports/validation/"
    assert payload["conventions"]["v0_7_spec"] == "openspec/changes/aetherstem-core-v0-7-adaptive-intelligence/"


def test_workflow_guidance_search():
    workflows = workflow_for("separate")

    assert workflows
    assert workflows[0]["name"] == "separate_stems"


def test_workflow_guidance_includes_validation():
    workflows = workflow_for("validate")

    assert workflows
    assert workflows[0]["name"] == "validate_platform"


def test_workflow_guidance_includes_adaptive_planning():
    workflows = workflow_for("adaptive")

    assert workflows
    assert workflows[0]["name"] == "adaptive_reconstruction_planning"
