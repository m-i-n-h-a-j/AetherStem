## ADDED Requirements

### Requirement: Short-Time Fourier Transform (STFT)
The system SHALL provide a utility to transform time-domain audio signals into the frequency domain using the Short-Time Fourier Transform.

#### Scenario: Successful STFT transformation
- **WHEN** a 96kHz floating-point audio buffer is passed to the STFT function
- **THEN** a complex-valued spectrogram matrix is returned with the specified window size and hop length

### Requirement: Inverse Short-Time Fourier Transform (ISTFT)
The system SHALL provide a utility to reconstruct time-domain audio signals from frequency-domain spectrograms using the Inverse Short-Time Fourier Transform.

#### Scenario: Successful signal reconstruction
- **WHEN** a complex-valued spectrogram is passed to the ISTFT function
- **THEN** a time-domain audio buffer is returned that matches the original duration

### Requirement: Windowing Functions
The system SHALL support multiple windowing functions (e.g., Hann, Hamming) for spectral analysis.

#### Scenario: Hann window application
- **WHEN** the STFT is performed with the 'hann' window type
- **THEN** the signal is multiplied by a Hann window before the FFT operation
