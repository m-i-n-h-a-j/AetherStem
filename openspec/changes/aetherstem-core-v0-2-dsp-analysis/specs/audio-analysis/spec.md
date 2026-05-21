## ADDED Requirements

### Requirement: RMS Energy Calculation
The system SHALL calculate the Root Mean Square (RMS) energy for audio frames to measure signal power.

#### Scenario: RMS calculation
- **WHEN** an audio buffer is analyzed for RMS
- **THEN** a scalar value representing the average energy is returned

### Requirement: Peak Level Detection
The system SHALL identify the absolute peak sample value in an audio signal for headroom analysis.

#### Scenario: Peak detection
- **WHEN** a buffer with values between -0.8 and +0.9 is analyzed
- **THEN** the peak value is reported as 0.9

### Requirement: Spectrogram Data Generation
The system SHALL generate magnitude spectrogram data for visual representation of frequency content.

#### Scenario: Spectrogram generation
- **WHEN** magnitude data is extracted from an STFT result
- **THEN** a real-valued matrix is returned suitable for visualization
