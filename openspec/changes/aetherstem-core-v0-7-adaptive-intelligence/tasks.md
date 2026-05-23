## 1. Artifact Intelligence

- [x] Add artifact detection records with confidence, severity, temporal/spectral region, strategy, and recoverability.
- [x] Add deterministic artifact heatmap summaries.
- [x] Bridge v0.6 forensic analysis into v0.7 artifact intelligence.
- [ ] Add dedicated detectors for pre-echo, warbling, pumping, aliasing, and ambience denormalization.

## 2. Adaptive Reconstruction

- [x] Add region classification primitives.
- [x] Add confidence-gated module policies.
- [ ] Integrate confidence gates into reconstruction graph building.
- [ ] Add dynamic graph mutation based on region maps and artifact heatmaps.

## 3. Temporal and Perceptual Stability

- [x] Add temporal stability report.
- [x] Add psychoacoustic perceptual report.
- [ ] Feed stability/perceptual scores into reconstruction reports.
- [ ] Add visual failure plots through the validation framework.

## 4. Runtime Scalability

- [x] Add hardware profiler and hardware tiers.
- [x] Add quality scaler with hardware clamping.
- [x] Add adaptive scheduler and memory planner.
- [x] Add backend selection contracts.
- [ ] Integrate hardware plans with CLI runtime options.

## 5. Determinism and Benchmarking

- [x] Add runtime graph node descriptors and reproducibility fingerprinting.
- [x] Add controlled degradation benchmark corpus primitives.
- [ ] Add graph fingerprints to reconstruction reports.
- [ ] Add long-form and backend-equivalence validation suites.
