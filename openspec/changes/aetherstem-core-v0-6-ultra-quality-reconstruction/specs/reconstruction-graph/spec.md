## ADDED Requirements

### Requirement: Adaptive Reconstruction Graph
The system SHALL generate a deterministic reconstruction graph from forensic profiles and selected reconstruction profile.

#### Scenario: Clipping detected
- **WHEN** the artifact profile reports clipping
- **THEN** the reconstruction graph includes a declip stage

### Requirement: Telemetry-Aware Stages
All reconstruction stages SHALL emit telemetry/profiling data when enabled.

#### Scenario: Multi-stage reconstruction
- **WHEN** reconstruction runs with telemetry enabled
- **THEN** each stage records timing and diagnostics

### Requirement: Multi-Pass Reconstruction
The subsystem SHALL support reproducible multi-pass reconstruction.

#### Scenario: Archival profile
- **WHEN** archival reconstruction is selected
- **THEN** the pipeline can execute analysis, restoration, bandwidth reconstruction, mastering, and perceptual optimization passes
