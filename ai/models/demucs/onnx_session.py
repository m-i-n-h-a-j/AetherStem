from __future__ import annotations

from pathlib import Path

import numpy as np

from ai.backends.onnx_runtime import OnnxRuntimeBackend
from ai.runtime.context import ExecutionContext


class DemucsOnnxSession:
    def __init__(self, model_path: Path, backend: OnnxRuntimeBackend | None = None) -> None:
        self.model_path = model_path
        self.backend = backend or OnnxRuntimeBackend()

    def run(self, chunk: np.ndarray, context: ExecutionContext) -> tuple[np.ndarray | list[np.ndarray], ExecutionContext]:
        session, prepared = self.backend.session(self.model_path, context)
        input_name = session.get_inputs()[0].name
        outputs = session.run(None, {input_name: chunk[np.newaxis, ...].astype(np.float32, copy=False)})
        if len(outputs) == 1:
            return outputs[0], prepared
        return outputs, prepared

