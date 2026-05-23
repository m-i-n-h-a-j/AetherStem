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
        {
            "name": "validate_platform",
            "intent": "Run static, unit, DSP, golden-reference, and report validation before release.",
            "commands": ["python -m validation.run_full_validation --quick"],
        },
        {
            "name": "reconstruct_master",
            "intent": "Create a plausibly reconstructed high-resolution master.",
            "commands": [
                "aetherstem forensic INPUT",
                "aetherstem reconstruct INPUT --profile extreme --target-rate 192000 --multi-pass --bandwidth-extension",
            ],
        },
        {
            "name": "archival_restore",
            "intent": "Run conservative archival reconstruction and render.",
            "commands": ["aetherstem archival INPUT --target-rate 192000"],
        },
    ]


def workflow_for(topic: str) -> list[dict]:
    topic = topic.lower()
    return [item for item in workflow_metadata() if topic in item["name"] or topic in item["intent"].lower()]
