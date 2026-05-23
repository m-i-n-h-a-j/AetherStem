## ADDED Requirements

### Requirement: Adaptive Chunk Scheduling
The runtime SHALL create deterministic chunk plans with chunk size, overlap, hop size, padding, batch size, estimated memory, and fallback mode.

#### Scenario: Default chunk plan
- **WHEN** a model receives audio shorter than the configured chunk size
- **THEN** the scheduler creates one padded chunk and trims padding after reconstruction

### Requirement: VRAM-Aware Batching
The scheduler SHALL use memory estimates and backend memory hints to choose batch size and chunk size.

#### Scenario: Limited VRAM
- **WHEN** estimated memory exceeds available memory
- **THEN** the scheduler reduces batch size or chunk size before inference starts

### Requirement: OOM Fallback
The runtime SHALL handle backend OOM failures by reducing batch size, reducing chunk size, or falling back to sequential CPU execution when policy allows.

#### Scenario: GPU OOM
- **WHEN** CUDA inference fails with an OOM condition
- **THEN** the runtime retries with a safer schedule or CPU fallback instead of crashing the full workflow

### Requirement: Deterministic Overlap-Add
Overlap-add reconstruction SHALL be deterministic and preserve expected duration.

#### Scenario: Reconstruct scheduled chunks
- **WHEN** chunks are overlap-added
- **THEN** repeated runs with the same inputs produce identical output samples within numeric tolerance
