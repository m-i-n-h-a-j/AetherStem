# Runtime Lifecycle

AetherStem v0.4 executes model work through a runtime boundary below orchestration.

```text
CLI/config -> orchestration graph -> runtime adapter -> execution context -> backend -> chunk scheduler -> reconstruction
```

The graph decides which stage should run. Runtime adapters execute inference only; they do not inspect files, run DSP analysis, export reports, or make routing decisions.

Core runtime types:

- `AudioBuffer`: canonical audio samples with sample rate, channel count, dtype, layout, and metadata.
- `ExecutionContext`: backend, device, provider, precision, low-memory mode, fallback policy, diagnostics, progress, and cancellation.
- `ChunkScheduler`: deterministic chunk planning with overlap, hop size, padding, estimated memory, and batch sizing.
- `ProgressReporter`: records and forwards progress events.
- `CancellationToken`: raises a structured cancellation error between chunks.

v0.5 extends this with:

- manifest-based model discovery and resolution;
- cache/checksum lifecycle diagnostics;
- runtime profile selection;
- precision policy;
- structured telemetry events;
- runtime profiling spans;
- AI-readable CLI metadata and troubleshooting guidance.
