## ADDED Requirements

### Requirement: One-command validation runner

The system SHALL provide a single command that runs static validation, unit tests, DSP verification, golden-reference checks, and report generation.

#### Scenario: Full validation run

- **WHEN** `python -m validation.run_full_validation` is executed
- **THEN** the system SHALL write JSON and HTML reports under `reports/validation`
- **AND** the process SHALL exit non-zero if any required check fails.

### Requirement: Deterministic synthetic audio lab

The system SHALL generate deterministic synthetic audio fixtures for DSP validation.

#### Scenario: Fixture determinism

- **WHEN** the synthetic suite is generated twice with the same parameters
- **THEN** fixture names and checksums SHALL match exactly.

### Requirement: Golden-reference comparison

The system SHALL compare candidate audio against golden references using waveform, spectral, RMS, phase, and temporal metrics.

#### Scenario: Drift detection

- **WHEN** candidate audio differs beyond configured tolerance
- **THEN** the comparison SHALL fail and include metric-level failure details.

### Requirement: Validation matrix generation

The system SHALL automatically generate combinational validation cases across pipeline, backend, precision, quality, device, chunk size, and streaming dimensions.

#### Scenario: Matrix generation

- **WHEN** validation axes are provided
- **THEN** the system SHALL return the Cartesian product as stable case identifiers.

### Requirement: Report contract

Validation reports SHALL have a deterministic JSON contract.

#### Scenario: Report schema validation

- **WHEN** a validation report is produced
- **THEN** it SHALL include version, started_at, passed, summary, and checks fields.
