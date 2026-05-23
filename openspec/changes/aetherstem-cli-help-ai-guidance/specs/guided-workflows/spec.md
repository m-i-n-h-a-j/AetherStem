## ADDED Requirements

### Requirement: Workflow Guidance
The CLI SHALL provide guided workflow recommendations for common tasks.

#### Scenario: Stem separation guidance
- **WHEN** the user requests guidance for separating stems
- **THEN** the CLI recommends `separate`, runtime diagnostics, model configuration, and benchmark options

### Requirement: Example Generation
The help system SHALL generate examples for common commands and runtime configurations.

#### Scenario: CPU runtime example
- **WHEN** examples are requested for separation on CPU
- **THEN** the CLI includes a command using `--backend onnx --device cpu`

### Requirement: Non-Executing Guidance
Guidance commands SHALL NOT run DSP analysis, model inference, exports, or benchmarks.

#### Scenario: Workflow help
- **WHEN** workflow guidance is displayed
- **THEN** no audio processing side effects occur
