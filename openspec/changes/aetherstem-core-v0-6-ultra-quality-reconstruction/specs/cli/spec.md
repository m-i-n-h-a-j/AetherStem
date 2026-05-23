## ADDED Requirements

### Requirement: Reconstruction CLI Commands
The CLI SHALL provide `reconstruct`, `remaster`, `archival`, `forensic`, and `upscale` commands.

#### Scenario: Extreme reconstruction
- **WHEN** the user runs `aetherstem reconstruct song.mp3 --profile extreme --target-rate 192000 --multi-pass`
- **THEN** the system runs forensic analysis, adaptive graph generation, reconstruction, evaluation, and high-resolution rendering

### Requirement: Forensic CLI Command
The CLI SHALL provide forensic analysis without running reconstruction.

#### Scenario: Forensic report
- **WHEN** the user runs `aetherstem forensic input.mp3`
- **THEN** a deterministic forensic JSON report is generated

### Requirement: Reconstruction Help
CLI help and AI metadata SHALL include reconstruction commands and examples.

#### Scenario: AI metadata export
- **WHEN** `aetherstem ai-metadata` is exported
- **THEN** reconstruction commands and workflow guidance are included
