## Why

Following the establishment of the AetherStem foundation in v0.1, the project now requires a robust Digital Signal Processing (DSP) and analysis engine. This engine is the prerequisite for AI-assisted source separation, enabling frequency-domain processing and providing deeper "audio intelligence" beyond basic file metadata.

## What Changes

- **Frequency Domain Processing**: Implement Short-Time Fourier Transform (STFT) and Inverse STFT (ISTFT) utilities.
- **Audio Intelligence**: Add features for RMS energy calculation, peak detection, and gain normalization.
- **Visual Analysis**: Generate spectrogram data structures for future UI/CLI visualization.
- **Smart Inspection**: Extend the CLI to provide deep technical analysis of audio content (e.g., dynamic range, spectral balance).

## Capabilities

### New Capabilities
- `dsp-transforms`: core frequency-domain transformations (STFT, ISTFT) and windowing logic.
- `audio-analysis`: high-level audio feature extraction (RMS, Peak, Loudness).
- `audio-intelligence`: intelligent insights and normalization logic.

### Modified Capabilities
- `cli`: Extend the `inspect` command or add a `deep-inspect` command for technical analysis.
- `audio_io`: Ensure I/O handles raw floating-point data streams for the DSP pipeline.

## Impact

This change adds significant math and signal processing logic to the `dsp/` and `utils/` packages. It introduces `librosa` and `scipy` as heavily used dependencies for core transformations. The CLI will become more powerful, transitioning from a basic metadata viewer to a technical audio analysis tool.
