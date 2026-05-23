## ADDED Requirements

### Requirement: Strict Runtime Adapter Interfaces
The system SHALL define inference-only runtime interfaces for separation, denoise, and enhancement adapters.

#### Scenario: Adapter boundary enforcement
- **WHEN** a runtime adapter executes
- **THEN** it performs inference only and does not run DSP analysis, write exports, read input files, or make orchestration decisions

### Requirement: Async Adapter Execution
Runtime adapters SHALL expose async load and inference methods.

#### Scenario: Synchronous CLI execution
- **WHEN** a synchronous CLI command runs an adapter
- **THEN** a runtime executor owns the async event-loop boundary while preserving async adapter contracts

### Requirement: Chunked Inference Support
Runtime adapters SHALL support chunked inference and report progress per chunk or batch.

#### Scenario: Separation in chunks
- **WHEN** a source separation model receives long audio
- **THEN** the adapter processes scheduled chunks and reconstructs outputs without changing the expected duration

### Requirement: Stream-Safe Processing
Runtime adapters SHALL be safe to call from generator-based stream pipelines.

#### Scenario: Streaming chunk source
- **WHEN** chunks are produced by the streaming pipeline
- **THEN** the adapter can consume chunks incrementally without file IO assumptions
