# Orchestration

The decision engine is deterministic and rule-based. It consumes structured analysis and lossy-detection results, then records each stage decision with observed values and thresholds.

Current rules:

- Enable denoise when `noise_floor_db` is above the configured threshold.
- Enable declip when clipping samples are detected.
- Enable enhancement when lossy/transcode confidence exceeds the configured threshold.
- Enable separation when the workflow explicitly requests it.
- Always validate and export graph results.

`AudioGraph` executes stages with typed boundaries and records skipped or completed stages in the run manifest. Validation rejects destructive output when new clipping or artifact scores exceed configured thresholds.

Presets are YAML files in `presets/` and resolve to a workflow, forced stages, thresholds, and graph configuration.

