## ADDED Requirements

### Requirement: Ultra-Quality Rendering
The system SHALL render float-safe outputs at high target sample rates including 96kHz and 192kHz.

#### Scenario: Archival render
- **WHEN** archival output is requested
- **THEN** the renderer writes a 32-bit float high-sample-rate file with deterministic headroom handling

### Requirement: Reconstruction Evaluation
The system SHALL score reconstruction quality, artifact reduction, spectral recovery, stereo integrity, transient quality, and mastering consistency.

#### Scenario: Reconstruction complete
- **WHEN** a reconstruction workflow finishes
- **THEN** evaluation metrics are included in the JSON report

### Requirement: Visual Diagnostics
The system SHALL generate optional before/after diagnostics such as spectrograms, waveform comparisons, stereo plots, and phase integrity artifacts.

#### Scenario: Diagnostic export
- **WHEN** visual diagnostics are enabled
- **THEN** before/after artifacts are written without requiring a GUI backend
