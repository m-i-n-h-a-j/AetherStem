## ADDED Requirements

### Requirement: Gain Normalization
The system SHALL provide a utility to normalize audio gain to a target peak level (e.g., -1.0 dBFS).

#### Scenario: Normalization to peak
- **WHEN** a signal with peak 0.5 is normalized to 1.0
- **THEN** all samples are scaled by a factor of 2.0

### Requirement: Dynamic Range Analysis
The system SHALL estimate the dynamic range of an audio file by comparing peak and RMS levels.

#### Scenario: Dynamic range calculation
- **WHEN** peak and RMS values are provided
- **THEN** the Crest Factor is calculated and reported in decibels (dB)
