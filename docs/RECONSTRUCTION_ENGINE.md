# Reconstruction Engine

AetherStem v0.6 adds an offline-quality reconstruction subsystem under `ai/reconstruction/`.

The philosophy is explicit: AetherStem does not perform true lossless recovery from lossy sources. It performs reconstruction, restoration, regeneration, remastering, spectral repair, and perceptual optimization to produce plausibly reconstructed high-resolution masters.

Pipeline:

```text
Input audio
  -> forensic analysis
  -> artifact profile
  -> restoration feasibility
  -> adaptive reconstruction graph
  -> optional multi-pass refinement
  -> high-resolution rendering
  -> evaluation and JSON reports
```

CLI commands:

```bash
aetherstem forensic input.mp3
aetherstem reconstruct input.mp3 --profile extreme --target-rate 192000 --multi-pass
aetherstem remaster input.flac
aetherstem archival input.wav
aetherstem upscale input.flac
```

Profiles:

- `fast`
- `balanced`
- `extreme`
- `archival`
- `experimental`

The first implementation is deterministic and DSP-first with runtime/model hooks for future restoration, bandwidth extension, mastering, declipping, harmonic synthesis, and transient reconstruction models.
