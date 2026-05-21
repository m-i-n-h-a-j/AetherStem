## ADDED Requirements

### Requirement: Restore Command
The CLI SHALL provide `aetherstem restore <input>` to run analysis-driven restoration and export restored audio plus reports.

#### Scenario: Restoring a damaged file
- **WHEN** the user runs `aetherstem restore damaged.flac`
- **THEN** the system analyzes the file, selects required processing stages, validates output, and writes exports

### Requirement: Separate Command
The CLI SHALL provide `aetherstem separate <input>` to generate separated stems.

#### Scenario: Separating stems
- **WHEN** the user runs `aetherstem separate song.flac`
- **THEN** `vocals.wav`, `drums.wav`, `bass.wav`, and `other.wav` are exported

### Requirement: Denoise Command
The CLI SHALL provide `aetherstem denoise <input>` to perform configurable broadband noise reduction.

#### Scenario: Denoising noisy audio
- **WHEN** the user runs `aetherstem denoise noisy.wav`
- **THEN** denoised audio and a validation report are exported

### Requirement: Enhance Command
The CLI SHALL provide `aetherstem enhance <input>` to perform validation-aware bandwidth extension or super-resolution when analysis warrants it.

#### Scenario: Enhancing lossy audio
- **WHEN** the user runs `aetherstem enhance lossy.mp3`
- **THEN** enhancement is applied only when analysis indicates likely benefit

### Requirement: Preset Command
The CLI SHALL provide `aetherstem preset <preset-name> <input>` for YAML-defined workflows.

#### Scenario: Running archival restore
- **WHEN** the user runs `aetherstem preset archival_restore input.flac`
- **THEN** the archival restore preset is validated and executed

### Requirement: Benchmark Command
The CLI SHALL provide `aetherstem benchmark <input>` to measure processing performance and quality metrics.

#### Scenario: Benchmarking a file
- **WHEN** the user runs `aetherstem benchmark input.flac`
- **THEN** runtime, memory, latency, SNR/SDR where available, and artifact scores are reported
