from __future__ import annotations


def workflow_metadata() -> list[dict]:
    return [
        {
            "name": "analyze_audio",
            "intent": "Inspect source quality before processing.",
            "commands": ["aetherstem inspect INPUT", "aetherstem analyze INPUT"],
        },
        {
            "name": "separate_stems",
            "intent": "Export vocals, drums, bass, and other stems.",
            "commands": ["aetherstem runtime-diagnostics", "aetherstem separate INPUT --backend onnx --device cpu"],
        },
        {
            "name": "restore_audio",
            "intent": "Run DSP-driven restoration and validation.",
            "commands": ["aetherstem restore INPUT", "aetherstem preset archival_restore INPUT"],
        },
        {
            "name": "debug_runtime",
            "intent": "Diagnose optional runtime/backend/model setup.",
            "commands": ["aetherstem runtime-diagnostics", "aetherstem model-registry", "aetherstem config-info ai"],
        },
    ]


def workflow_for(topic: str) -> list[dict]:
    topic = topic.lower()
    return [item for item in workflow_metadata() if topic in item["name"] or topic in item["intent"].lower()]

