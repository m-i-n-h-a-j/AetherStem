## ADDED Requirements

### Requirement: Hardware Capability Probe
The runtime SHALL probe CPU, CUDA, DirectML-ready hooks, provider availability, precision support, and memory summaries.

#### Scenario: Runtime diagnostics
- **WHEN** runtime diagnostics are requested
- **THEN** the CLI reports hardware capabilities, backend capabilities, provider status, and memory summaries where available

### Requirement: Runtime Profiles
The runtime SHALL define deterministic runtime profiles such as `cpu_safe`, `cuda_fast`, `cuda_low_memory`, `portable`, and `diagnostic`.

#### Scenario: Portable profile
- **WHEN** the portable profile is selected
- **THEN** runtime selection prefers broadly available CPU-safe execution and records that profile

### Requirement: Hardware-Aware Model Compatibility
Model resolution SHALL consider available hardware and backend provider capabilities.

#### Scenario: CUDA-only model on CPU system
- **WHEN** a CUDA-only manifest is resolved on a CPU-only system
- **THEN** the resolver rejects it with a structured compatibility reason

### Requirement: Deterministic Preset Selection
Automatic runtime preset selection SHALL be deterministic for a given hardware profile and configuration.

#### Scenario: Auto runtime profile
- **WHEN** auto profile selection runs twice on the same system and config
- **THEN** it selects the same profile and records the same decision path
