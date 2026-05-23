# Chunk Scheduler

`ChunkScheduler` creates a `ChunkPlan` containing:

- chunk size
- overlap
- hop size
- batch size
- total samples
- padded samples
- estimated memory
- chunk descriptors

Chunks are padded for model-compatible execution and trimmed during overlap-add reconstruction. `overlap_add()` is deterministic and duration-preserving for repeated runs with the same inputs.

Low-memory mode forces sequential batching and is intended for long files or constrained systems.

