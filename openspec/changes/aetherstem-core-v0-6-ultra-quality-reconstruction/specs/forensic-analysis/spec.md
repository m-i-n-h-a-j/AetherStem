## ADDED Requirements

### Requirement: Deterministic Forensic Source Analysis
The system SHALL generate deterministic source, artifact, spectral fingerprint, feasibility, and confidence reports.

#### Scenario: 128kbps MP3-style source
- **WHEN** analysis detects spectral cutoff, codec ringing, transient softening, and stereo collapse
- **THEN** the forensic report exposes likely source, detected artifacts, restoration potential, and confidence

### Requirement: Transparent Uncertainty
Forensic reports SHALL expose confidence and uncertainty for source classification and restoration potential.

#### Scenario: Ambiguous source
- **WHEN** evidence is mixed
- **THEN** the report uses moderate or low confidence instead of absolute claims

### Requirement: JSON Export
Forensic reports SHALL be JSON serializable.

#### Scenario: CLI forensic command
- **WHEN** `aetherstem forensic input.mp3` completes
- **THEN** a JSON forensic report is written under the output directory
