## ADDED Requirements

### Requirement: Harmonic Regeneration
The system SHALL provide phase-aware harmonic regeneration with tonal balance preservation.

#### Scenario: Missing high overtones
- **WHEN** a source has high-frequency loss
- **THEN** harmonic regeneration can synthesize controlled overtones without claiming original recovery

### Requirement: Spectral Repair
The system SHALL provide spectral interpolation, notch repair, ringing suppression, hole filling, smoothing, and continuity repair hooks.

#### Scenario: Codec notch
- **WHEN** a spectral notch is detected
- **THEN** spectral repair can interpolate surrounding context deterministically

### Requirement: Stereo Reconstruction
The system SHALL provide stereo repair while preserving mono compatibility and center image integrity.

#### Scenario: Joint stereo collapse
- **WHEN** stereo collapse is detected
- **THEN** the graph may enable stereo reconstruction without fake widening by default

### Requirement: AI Mastering
The system SHALL provide mastering profiles for transparent, hifi, cinematic, studio, and archival outputs.

#### Scenario: Archival mastering
- **WHEN** archival profile is selected
- **THEN** mastering preserves dynamics and avoids overcompression
