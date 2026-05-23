# Backend Abstraction

Runtime backends are discovered through `ai.backends.registry.BackendRegistry`.

Implemented backends:

- `onnx`: ONNX Runtime session management, provider discovery, CPU/CUDA provider selection, and fp16 preference diagnostics.
- `torch`: optional fallback runtime boundary with CPU/CUDA device diagnostics.

Provider selection is deterministic:

1. Use an explicitly requested provider when available.
2. Use CUDA when requested and available.
3. Fall back to CPU only when fallback policy allows it.
4. Raise a structured runtime error when no compatible provider exists.

Use `aetherstem runtime-diagnostics` to inspect backend availability.

