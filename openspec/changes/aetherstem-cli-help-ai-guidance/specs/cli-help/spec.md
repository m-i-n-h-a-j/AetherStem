## ADDED Requirements

### Requirement: Contextual Help Command
The CLI SHALL provide `aetherstem help [topic]` for contextual command and topic help.

#### Scenario: Help for separation
- **WHEN** the user runs `aetherstem help separate`
- **THEN** the CLI shows separation usage, runtime flags, examples, related commands, and troubleshooting hints

### Requirement: Topic Discovery
The help system SHALL support topic aliases such as runtime, models, config, benchmark, restore, and separate.

#### Scenario: Runtime help
- **WHEN** the user runs `aetherstem help runtime`
- **THEN** the CLI explains runtime backends, devices, chunking, diagnostics, and model path behavior

### Requirement: Runtime-Aware Help
Help output SHALL include lightweight runtime-aware recommendations without loading model weights.

#### Scenario: ONNX unavailable
- **WHEN** runtime help is requested on a system without ONNX Runtime
- **THEN** help can recommend installing the runtime CPU extra without failing
