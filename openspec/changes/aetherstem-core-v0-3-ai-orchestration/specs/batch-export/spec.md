## ADDED Requirements

### Requirement: Structured Export Directory
The system SHALL export restored audio, separated stems, analysis reports, validation reports, comparison reports, previews, and run manifests under `exports/` by default.

#### Scenario: Restore export
- **WHEN** a restore workflow succeeds
- **THEN** the export directory contains restored audio, JSON reports, previews, and a manifest with model/backend/config details

### Requirement: Rejected Output Isolation
The system SHALL keep rejected processed outputs separate from accepted final exports.

#### Scenario: Validation rejection
- **WHEN** validation rejects enhanced audio
- **THEN** the rejected artifact is not written as the final restored output and the report records the rejection

### Requirement: Batch Processing
The CLI SHALL provide `aetherstem batch <folder>` to recursively process supported audio files.

#### Scenario: Recursive folder processing
- **WHEN** the user runs `aetherstem batch ./music/`
- **THEN** supported audio files under the folder are queued and processed with isolated per-file results

### Requirement: Resumable Jobs
Batch processing SHALL persist queue state so interrupted work can resume without reprocessing completed files.

#### Scenario: Resume interrupted batch
- **WHEN** a batch run is restarted after interruption
- **THEN** completed files are skipped unless the user requests reprocessing

### Requirement: Benchmark Reports
The benchmarking framework SHALL write structured benchmark reports under `benchmarks/` or the configured output directory.

#### Scenario: Benchmark export
- **WHEN** benchmark execution completes
- **THEN** a report containing runtime, device, memory, latency, and quality metrics is saved
