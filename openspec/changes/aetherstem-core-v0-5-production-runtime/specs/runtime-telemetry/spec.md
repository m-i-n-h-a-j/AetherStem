## ADDED Requirements

### Requirement: Structured Runtime Events
The runtime SHALL emit structured telemetry events for model resolution, cache validation, backend selection, provider selection, precision selection, chunk planning, fallback, OOM handling, cancellation, and completion.

#### Scenario: Backend fallback
- **WHEN** execution falls back from CUDA to CPU
- **THEN** telemetry records the original request, fallback target, reason, and timestamp

### Requirement: Trace Spans
The runtime SHALL support trace spans for stage-level and chunk-level timing.

#### Scenario: Chunk profiling
- **WHEN** profiling is enabled for separation
- **THEN** each chunk can produce a trace span with start time, end time, stage, and diagnostics

### Requirement: Manifest Integration
Telemetry summaries SHALL be included in export manifests when telemetry is enabled.

#### Scenario: Telemetry-enabled export
- **WHEN** a runtime workflow completes with telemetry enabled
- **THEN** the export manifest references or embeds a telemetry summary

### Requirement: Bounded Telemetry
Telemetry SHALL remain bounded for long-running streaming workflows.

#### Scenario: Long streaming job
- **WHEN** thousands of chunks are processed
- **THEN** telemetry stores summaries or bounded event windows according to configuration
