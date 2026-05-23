# Model Integration

v0.3 models implement `ai.models.base.AudioModel`:

```python
class AudioModel(Protocol):
    name: str
    version: str
    metadata: ModelMetadata

    def load(self) -> None: ...
    def process(self, audio, sample_rate, config=None) -> ModelResult: ...
```

Register models through `ModelRegistry.register(metadata, factory)`. Metadata is lightweight and available at startup; model weights and heavy imports belong inside `load()` or adapter-local execution code.

Compatibility is checked before inference with backend and device requirements from `ModelRequirements`. Incompatible selections raise structured errors before audio processing starts.

Built-in adapter families:

- Demucs-compatible separation
- MDX/UVR-compatible ONNX separation
- DeepFilterNet/RNNoise-style denoise
- Enhancement and bandwidth extension
- Super-resolution

## v0.4 Runtime Adapters

New executable integrations should implement the runtime interfaces in `ai/adapters/` instead of placing inference directly in orchestration.

Rules:

- adapters are inference-only;
- no DSP analysis;
- no export logic;
- no file IO for user inputs or reports;
- async load and execution methods;
- accept `AudioBuffer` and `ExecutionContext`;
- support progress, cancellation, chunked execution, and stream-safe processing.

Separation models implement `SeparationAdapter`. The Demucs-compatible runtime adapter lives in `ai/models/demucs/runtime_adapter.py` and prefers ONNX Runtime when a model path is configured.
