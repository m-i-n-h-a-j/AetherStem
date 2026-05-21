## Context

AetherStem v0.1 established the environment, logging, and basic FFmpeg-based audio conversion. v0.2 introduces the "Brain" of the DSP pipeline. To separate audio sources, we must first be able to analyze them in both time and frequency domains. This design covers the implementation of core signal transforms and high-level audio intelligence features.

## Goals / Non-Goals

**Goals:**
- Standardize STFT/ISTFT parameters (window size, hop length) across the project.
- Provide high-level analysis utilities for Peak, RMS, and Dynamic Range.
- Integrate these utilities into a new `deep-inspect` CLI command.
- Ensure the pipeline can load audio directly into NumPy buffers.

**Non-Goals:**
- Real-time or low-latency audio processing.
- GPU-accelerated FFT (CPU is sufficient for current requirements).
- Full source separation models (this is the preparatory phase).

## Decisions

- **Signal Transforms**: Use `librosa` for STFT and ISTFT. Librosa is the industry standard for AI audio research and provides robust handling of padding and centering.
- **I/O Optimization**: Implement `audio_io.load_raw` using the `soundfile` library. While FFmpeg is great for conversion, `soundfile` is much faster for direct reading of the 96kHz/32-bit float WAVs generated in v0.1 into NumPy arrays.
- **Feature Storage**: Audio features (RMS, Peak) will be calculated frame-by-frame but aggregated for analysis reports.
- **Windowing**: Default to the 'hann' window for all STFT operations as it provides a good balance between frequency resolution and spectral leakage.

## Risks / Trade-offs

- **[Risk] Memory Consumption** → **[Mitigation]** Spectrograms for long high-sample-rate files (96kHz) can be extremely large. The system will log a warning for files longer than 5 minutes and recommend processing in sections if memory issues occur.
- **[Trade-off] Librosa vs Custom FFT** → **[Rationale]** Librosa is chosen over raw NumPy FFT to benefit from specialized audio windowing and centering logic that is critical for perfect reconstruction (STFT -> ISTFT).
- **[Risk] Precision Loss** → **[Mitigation]** Use 64-bit complex numbers for the STFT matrix during internal calculations to maintain precision before returning 32-bit float results.
