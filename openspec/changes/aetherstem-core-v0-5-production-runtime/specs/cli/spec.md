## MODIFIED Requirements

### Requirement: Model Registry CLI
The CLI SHALL provide commands to list discovered model manifests, validate model cache, and resolve a model for a requested task/backend/device/precision.

#### Scenario: Listing manifests
- **WHEN** the user runs the model registry list command
- **THEN** the CLI prints local manifests without loading model weights

### Requirement: Extended Runtime Diagnostics
Runtime diagnostics SHALL include hardware profiles, backend capabilities, provider status, model registry status, cache status, and selected runtime preset.

#### Scenario: Diagnosing missing model
- **WHEN** no compatible model is available for separation
- **THEN** diagnostics explain whether the issue is discovery, compatibility, cache, checksum, backend, or precision related

### Requirement: Telemetry and Profiling Flags
Runtime CLI commands SHALL expose opt-in telemetry and profiling flags.

#### Scenario: Profiled runtime command
- **WHEN** the user enables profiling
- **THEN** the workflow writes a structured profiling report and references it from the manifest
