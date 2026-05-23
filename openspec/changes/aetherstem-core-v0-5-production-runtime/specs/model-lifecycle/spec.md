## ADDED Requirements

### Requirement: Model Cache Management
The runtime SHALL manage model asset cache paths separately from model execution.

#### Scenario: Resolving cached model path
- **WHEN** a manifest references a cached asset
- **THEN** the lifecycle manager resolves the path without loading the model

### Requirement: Checksum Validation
Model assets SHALL be validated with SHA-256 checksums before executable runtime use.

#### Scenario: Corrupt cached model
- **WHEN** a cached model file checksum does not match the manifest
- **THEN** execution is rejected with a structured cache-integrity error

### Requirement: Cache Diagnostics
The lifecycle manager SHALL report missing, corrupt, stale, and locked model cache states.

#### Scenario: Missing model asset
- **WHEN** a manifest is valid but the model file is absent
- **THEN** diagnostics explain the missing asset and recommend cache repair or download

### Requirement: Download Extension Points
The lifecycle layer SHALL expose interfaces for future downloads without requiring automatic remote downloads in v0.5.

#### Scenario: Downloadable model source
- **WHEN** a manifest includes a URL
- **THEN** the lifecycle manager can report it as downloadable metadata even if automatic download is disabled
