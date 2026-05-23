# Model Integration

Models implement `ai.models.base.AudioModel`:

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

