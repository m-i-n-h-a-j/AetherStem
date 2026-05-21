# AetherStem DSP Analysis Methodology

This document details the deterministic signal diagnostics and audio analysis pipeline implemented in AetherStem v0.2.

## 1. Overview
The AetherStem DSP pipeline is designed to provide professional-grade insights into audio quality, loudness, and spectral characteristics before any AI-based source separation.

## 2. Analysis Stages

### 2.1. Loudness Analysis
- **Standard:** EBU R128
- **Metrics:**
  - Integrated Loudness (LUFS)
  - Short-term Maximum Loudness (LUFS)
  - Momentary Maximum Loudness (LUFS)
  - Loudness Range (LRA)
  - True Peak (dBTP)
- **Implementation:** `pyloudnorm` with scipy-based 4x oversampling for True Peak estimation.

### 2.2. Spectral Analysis
- **Centroid:** "Center of mass" of the spectrum.
- **Rolloff:** Frequency below which a specified percentage of the total spectral energy lies.
- **HF Cutoff Detection:** Identifies the point where high-frequency energy drops significantly (>40dB below peak), used for lossy detection.

### 2.3. Lossy Source Detection
AetherStem uses heuristic-based analysis to detect if a "lossless" file (like FLAC or WAV) was actually transcoded from a lossy source (MP3, AAC).
- **MP3 128kbps:** Usually cut off at 16kHz.
- **MP3 192kbps:** Usually cut off at 18kHz.
- **MP3 320kbps:** Usually cut off at 20kHz.

### 2.4. Stereo & Phase Analysis
- **Stereo Width:** Calculated via Mid/Side energy ratio.
- **Phase Correlation:** Measures the similarity between L and R channels (-1.0 to 1.0) dynamically.
- **Vectorscope:** Visual representation of stereo distribution.

## 3. Visualization Engine
Generates publication-quality plots:
- **Spectrogram:** Time-frequency distribution.
- **Waveform:** Time-domain amplitude.
- **Vectorscope:** Stereo field distribution.
- **Phase Correlation Graph:** Shows phase correlation over time.

## 4. Caching System
To avoid redundant expensive FFT operations, results are cached based on the SHA256 hash of the input file content.

## 5. Limitations
- Heuristics for lossy detection may be fooled by intentionally low-pass filtered audio.
- Phase correlation is calculated over the entire file; local phase issues might be averaged out.

## 6. Future AI Integration
The `AudioModel` protocol in `models/base.py` defines the interface for future integration of models like Demucs or UVR.
