## ADDED Requirements

### Requirement: Runtime Benchmark Metrics
The benchmark framework SHALL record throughput, latency, memory usage, backend/provider selection, and chunk scheduler metrics.

#### Scenario: Runtime benchmark report
- **WHEN** a runtime-enabled command completes with benchmarking enabled
- **THEN** a structured benchmark report contains runtime duration, processed audio seconds per second, memory summary, backend, provider, chunk size, overlap, and batch size

### Requirement: Backend Comparison Reports
The benchmark framework SHALL support comparing compatible backends for the same model and input.

#### Scenario: Comparing CPU and CUDA
- **WHEN** both CPU and CUDA providers are available
- **THEN** benchmark reports can compare latency, throughput, and memory behavior for both providers

### Requirement: Scheduler Efficiency Metrics
The benchmark framework SHALL report chunk scheduler efficiency.

#### Scenario: Chunked inference benchmark
- **WHEN** inference runs in chunks
- **THEN** the report includes number of chunks, batch size, overlap overhead, fallback count, and retry count
