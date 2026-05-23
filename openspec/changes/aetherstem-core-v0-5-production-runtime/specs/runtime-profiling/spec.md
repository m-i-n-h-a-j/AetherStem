## ADDED Requirements

### Requirement: Runtime Profiling Reports
The benchmarking framework SHALL generate profiling reports with stage timings, chunk timings, memory snapshots where available, runtime profile, backend, provider, precision, model manifest, and cache status.

#### Scenario: Profiled separation
- **WHEN** separation runs with profiling enabled
- **THEN** a JSON profiling report is written with chunk scheduler and backend timing metrics

### Requirement: Backend Comparison
The profiler SHALL support comparing compatible runtime profiles and backends for the same model/input.

#### Scenario: CPU versus CUDA benchmark
- **WHEN** CPU and CUDA profiles are both compatible
- **THEN** benchmark output can compare throughput, latency, memory, and fallback counts

### Requirement: Production-Safe Profiling
Profiling SHALL be opt-in and safe for headless execution.

#### Scenario: CI benchmark
- **WHEN** profiling runs in a headless environment
- **THEN** it writes structured files without requiring a GUI or interactive display
