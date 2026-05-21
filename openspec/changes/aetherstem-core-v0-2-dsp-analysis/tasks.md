## 1. Enhanced I/O & Buffer Management

- [ ] 1.1 Implement `audio_io/buffer_loader.py` with `load_raw` function using `soundfile`
- [ ] 1.2 Update `audio_io/__init__.py` to expose raw loading utilities

## 2. Core DSP Transforms

- [ ] 2.1 Implement `dsp/transforms.py` with `stft` and `istft` wrappers using `librosa`
- [ ] 2.2 Add support for multiple window types (Hann, Hamming) in `dsp/transforms.py`
- [ ] 2.3 Implement STFT consistency check (verify padding and centering logic)

## 3. Audio Intelligence & Feature Extraction

- [ ] 3.1 Implement Peak and RMS energy calculation in `dsp/analysis.py`
- [ ] 3.2 Implement Dynamic Range (Crest Factor) calculation in `dsp/intelligence.py`
- [ ] 3.3 Implement Peak-based Gain Normalization utility
- [ ] 3.4 Add magnitude spectrogram extraction utility

## 4. CLI Expansion

- [ ] 4.1 Implement `deep-inspect` command in `cli/main.py`
- [ ] 4.2 Create rich formatting for technical analysis reports (Peak, RMS, Crest Factor)
- [ ] 4.3 Add a simple "Spectral Summary" to the deep inspection output

## 5. Verification & Testing

- [ ] 5.1 Create `tests/test_dsp.py` for verifying STFT/ISTFT perfect reconstruction
- [ ] 5.2 Create `tests/test_intelligence.py` for verifying normalization and feature extraction
- [ ] 5.3 Verify `deep-inspect` command functionality with test audio
