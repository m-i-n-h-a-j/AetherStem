## ADDED Requirements

### Requirement: Runtime Troubleshooting Assistant
The CLI SHALL provide troubleshooting guidance for runtime and model setup issues.

#### Scenario: Missing runtime dependency
- **WHEN** ONNX Runtime is unavailable
- **THEN** troubleshooting output recommends the appropriate runtime extra and explains affected commands

### Requirement: Config Introspection
The CLI SHALL expose current config values and schema-like summaries in human and JSON forms.

#### Scenario: Inspect AI config
- **WHEN** the user requests config introspection for AI settings
- **THEN** the CLI shows configured models, backend/device defaults, chunking, precision, and model path

### Requirement: Production-Safe Diagnostics
Diagnostics commands SHALL avoid loading model weights or running inference.

#### Scenario: Troubleshooting model path
- **WHEN** diagnostics checks a configured model path
- **THEN** it verifies path presence and reports status without creating a runtime session
