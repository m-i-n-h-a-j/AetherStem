## ADDED Requirements

### Requirement: Post-Process Validation
The system SHALL validate processed audio by comparing pre-process and post-process analysis metrics.

#### Scenario: Validation after enhancement
- **WHEN** enhancement completes
- **THEN** the system compares pre/post metrics and emits a structured validation decision

### Requirement: Artifact Detection
The validation layer SHALL score artifact confidence for metallic ringing, pre-echo, transient smearing, hallucinated harmonics, phase corruption, and unstable stereo image.

#### Scenario: High artifact confidence
- **WHEN** artifact confidence exceeds the configured rejection threshold
- **THEN** the processed output is marked rejected and the artifact report explains the reason

### Requirement: Quality Comparator
The system SHALL generate before/after comparison metrics for loudness delta, spectral restoration, noise reduction estimate, clipping reduction, stereo integrity, and dynamic range preservation.

#### Scenario: Comparison report export
- **WHEN** a restore workflow completes
- **THEN** a JSON comparison report is exported with all configured quality metrics

### Requirement: Destructive Enhancement Rejection
The system SHALL reject processed audio that introduces clipping, severe phase regression, excessive stereo instability, or dynamic range collapse.

#### Scenario: New clipping introduced
- **WHEN** processed audio contains clipping that was not present before processing
- **THEN** validation rejects the processed output unless configuration explicitly permits it
