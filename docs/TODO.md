# AetherStem Roadmap & TODOs

This document outlines the next steps for the AetherStem project after the initial core foundation.

## AI Model Integration
- [ ] Research and select base source separation models (e.g., Demucs, Hybrid Transformer).
- [ ] Implement model loading logic in `models/loader.py`.
- [ ] Set up CUDA/DirectML support for Windows-based GPU acceleration.
- [ ] Implement inference loop for processing audio chunks.

## DSP & Pipeline Development
- [ ] Implement Short-Time Fourier Transform (STFT) and Inverse STFT in `dsp/transforms.py`.
- [ ] Implement overlap-add reconstruction logic for seamless chunk processing.
- [ ] Add support for multiple stems (Drums, Bass, Other, Vocals).
- [ ] Implement post-processing filters for artifact reduction.

## CLI Enhancements
- [ ] Add progress bars for long-running processing tasks using `tqdm` or `rich.progress`.
- [ ] Implement batch processing for multiple files/directories.
- [ ] Add configuration override options via CLI flags.

## Testing & Validation
- [ ] Implement unit tests for audio I/O and conversion logic.
- [ ] Add integration tests for the full pipeline.
- [ ] Benchmarking on different hardware (CPU vs GPU).

## Documentation
- [ ] API documentation using Sphinx or MkDocs.
- [ ] User guide with examples and troubleshooting tips.
