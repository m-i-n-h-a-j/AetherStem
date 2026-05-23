## ADDED Requirements

### Requirement: Reconstruction Subsystem
The system SHALL provide `ai/reconstruction/` as a modular, reusable subsystem for offline-quality reconstruction, restoration, remastering, and archival rendering.

#### Scenario: Reusable reconstruction engine
- **WHEN** restore, enhance, remaster, archival, forensic, separate, or batch workflows need reconstruction
- **THEN** they can reuse reconstruction graph stages without duplicating orchestration logic

### Requirement: No True Lossless Recovery Claims
The system SHALL NOT describe lossy source processing as true lossless recovery.

#### Scenario: Lossy source report
- **WHEN** a lossy source is analyzed
- **THEN** reports describe reconstruction confidence and uncertainty rather than claiming original-master recovery

### Requirement: Profile-Driven Offline Quality
The reconstruction subsystem SHALL support fast, balanced, extreme, archival, and experimental profiles.

#### Scenario: Extreme profile
- **WHEN** the user selects extreme reconstruction
- **THEN** the graph may include multi-pass, harmonic, bandwidth, spectral, transient, psychoacoustic, and mastering stages
