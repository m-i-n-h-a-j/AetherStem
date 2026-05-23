## MODIFIED Requirements

### Requirement: Lightweight Base Install
The base package installation SHALL avoid mandatory heavyweight inference dependencies where possible.

#### Scenario: Installing analysis-only AetherStem
- **WHEN** the user installs the base package
- **THEN** deterministic DSP analysis and orchestration metadata remain available without requiring CUDA or heavyweight model runtimes

### Requirement: Runtime Optional Dependency Groups
The project SHALL define optional dependency groups for runtime CPU, runtime CUDA, and runtime development workflows.

#### Scenario: Installing CPU runtime
- **WHEN** the user installs the `runtime-cpu` extra
- **THEN** ONNX Runtime CPU execution dependencies are installed

### Requirement: Headless-Safe Execution
Runtime and benchmark workflows SHALL remain safe in headless environments.

#### Scenario: Running tests in CI
- **WHEN** runtime tests and benchmarks generate reports or previews
- **THEN** they do not require GUI backends or interactive display support
