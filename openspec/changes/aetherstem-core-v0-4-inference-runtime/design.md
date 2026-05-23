## Context

AetherStem v0.3 added a top-level `ai/` package with model metadata, registry, placeholder adapters, compute backend selection, orchestration, validation, export, presets, batch workflows, and benchmarking. The placeholders prove the graph shape but do not define enough runtime behavior for real source separation models. Real inference needs stable contracts for audio layout, tensor conversion, chunk scheduling, provider/session management, device memory, async lifecycle, cancellation, and progress.

v0.4 adds a runtime layer between orchestration and model adapters:

```text
Orchestration Graph
  -> Runtime Adapter Interface
  -> Execution Context
  -> Backend Registry
  -> ONNX / PyTorch Runtime
  -> Chunk Scheduler
  -> Reconstruction
```

The orchestration graph should continue to select stages and route by capability. It should not know whether a model uses ONNX Runtime, PyTorch, chunk batching, fp16, or fallback execution.

## Proposed Package Layout

```text
ai/
  runtime/
    __init__.py
    audio_buffer.py
    tensor_contracts.py
    device_manager.py
    memory_manager.py
    chunk_scheduler.py
    stream_pipeline.py
    progress.py
    cancellation.py
    context.py
  backends/
    __init__.py
    base.py
    registry.py
    onnx_runtime.py
    torch_runtime.py
  adapters/
    __init__.py
    base.py
    separation.py
    denoise.py
    enhancement.py
  models/
    demucs/
      runtime_adapter.py
      onnx_session.py
      torch_fallback.py
      reconstruction.py
```

The existing `ai/compute/` package MAY remain as a compatibility facade during migration, but new executable inference should use `ai/runtime/` and `ai/backends/`.

## Runtime Core

`AudioBuffer` is the canonical in-memory representation:

- `samples: np.ndarray`
- `sample_rate: int`
- `channels: int`
- `dtype: str`
- `layout: Literal["channels_first", "channels_last", "mono"]`
- `metadata: dict[str, Any]`

It provides explicit conversion helpers:

- `as_channels_first()`
- `as_channels_last()`
- `astype(dtype)`
- `duration_seconds`
- `validate()`

`tensor_contracts.py` defines movement between NumPy, Torch, and ONNX Runtime without adapter-specific ad hoc shape handling. Contracts define expected rank, layout, dtype, batch dimension, channel count, and padding behavior.

`ExecutionContext` records:

- backend id
- device id
- provider id
- precision preference
- low-memory mode
- fallback policy
- cancellation token
- progress reporter
- runtime diagnostics

## Runtime Adapter Interfaces

Adapters are inference-only. They SHALL NOT perform DSP analysis, export files, read user input files, write reports, or make orchestration decisions.

Runtime adapters expose async methods:

```python
class SeparationAdapter(Protocol):
    metadata: ModelMetadata

    async def load(self, context: ExecutionContext) -> None: ...

    async def separate(
        self,
        audio: AudioBuffer,
        context: ExecutionContext,
        options: SeparationOptions,
    ) -> SeparationResult: ...
```

Equivalent interfaces exist for denoise and enhancement. All adapters accept cancellation and progress via `ExecutionContext`, support chunked execution, and are stream-safe by construction.

Synchronous CLI commands may call adapters through a runtime executor that owns the event loop boundary.

## ONNX Runtime Backend

The ONNX backend owns:

- `InferenceSession` creation and caching.
- Provider detection.
- Provider preference and fallback.
- CPU and CUDA execution providers.
- Model input/output name discovery.
- Optional fp16 hooks.
- Structured provider diagnostics.

Provider selection must be deterministic:

1. honor explicit provider/device when available;
2. use CUDA when requested and available;
3. fall back to CPU only when fallback policy allows it;
4. return a structured unsupported-provider error otherwise.

## Demucs-Compatible Separation

The first executable model integration is Demucs-compatible separation with ONNX-preferred execution. The adapter accepts a local ONNX model path or registry-managed model reference. PyTorch fallback is optional and only used when configured and available.

Required behavior:

- Convert input to stereo channels-first runtime layout.
- Pad chunks to model-compatible frame sizes.
- Run chunk batches through ONNX Runtime.
- Reconstruct with deterministic overlap-add.
- Preserve duration after trimming padding.
- Export stem tensors through runtime result objects, not file IO.
- Support `vocals`, `drums`, `bass`, `other`, and optional `instrumental`.

## Chunk Scheduler

The scheduler produces a deterministic `ChunkPlan`:

- chunk size
- overlap
- hop size
- padding
- batch size
- estimated memory
- fallback mode

It uses runtime memory hints to choose batch size and chunk size. If a backend reports OOM or insufficient memory, the scheduler should reduce batch size, then chunk size, then fall back to sequential CPU execution when policy allows.

Overlap-add must be deterministic and tested independently from model inference.

## Streaming Pipeline

Streaming in v0.4 means low-memory generator-based processing, not realtime microphone capture. The stream pipeline should:

- emit scheduled chunks from an `AudioBuffer` or source iterator;
- run inference incrementally;
- reconstruct incrementally;
- support cancellation between chunks;
- keep bounded memory in low-memory mode.

The API should leave room for future realtime processing without requiring realtime guarantees now.

## CLI

AI commands should accept runtime flags:

- `--device cpu|cuda|auto`
- `--backend onnx|torch|auto`
- `--chunk-size <samples>`
- `--overlap <ratio>`
- `--low-memory`
- `--benchmark-runtime`

Add a runtime diagnostics command that reports:

- available backends;
- ONNX Runtime providers;
- Torch CUDA availability;
- selected device/provider;
- memory summary where available;
- optional dependency availability.

## Packaging

Base install should remain lightweight. Add optional dependency groups:

- `runtime-cpu`: ONNX Runtime CPU execution and runtime utilities.
- `runtime-cuda`: CUDA-capable runtime packages where installable through Python packaging.
- `runtime-dev`: test and benchmark tooling for runtime development.

PyTorch should not be required by the base install unless another core dependency requires it.

## Risks / Trade-offs

- **Model format variability**: isolate model-specific assumptions inside adapters and tensor contracts.
- **Provider availability differences**: expose diagnostics and deterministic fallback behavior.
- **OOM behavior**: adaptive scheduling can reduce failure rate, but cannot guarantee success for all files/models.
- **Async complexity**: keep CLI sync by using a runtime executor boundary while enforcing async adapter contracts internally.
- **Package churn**: preserve v0.3 orchestration APIs while introducing runtime interfaces below them.
