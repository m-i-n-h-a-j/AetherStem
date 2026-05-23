## ADDED Requirements

### Requirement: Typed Model Manifests
The system SHALL represent runtime models with strongly typed manifests containing model id, semantic version, architecture, task, backend compatibility, precision support, sample rate, channel count, stems, checksum, and model format.

#### Scenario: Parsing a local manifest
- **WHEN** a local model manifest is discovered
- **THEN** it is parsed into a typed manifest object and schema validation errors are reported structurally

### Requirement: Deterministic Model Discovery
The registry SHALL discover local manifests from configured directories in deterministic order.

#### Scenario: Multiple local manifests
- **WHEN** two compatible manifests are present
- **THEN** discovery order and resolver tie-breaking are stable across runs

### Requirement: Lazy Model Resolution
Model resolution SHALL return metadata and asset paths without importing runtime packages or loading model weights.

#### Scenario: Listing available models
- **WHEN** the user lists model manifests
- **THEN** metadata is available without initializing ONNX Runtime, Torch, or model sessions

### Requirement: Future Remote Registry Compatibility
The registry SHALL include source metadata and resolver extension points compatible with future remote registries.

#### Scenario: Remote source metadata
- **WHEN** a manifest references a remote source
- **THEN** the registry records the source without requiring a hosted registry service in v0.5
