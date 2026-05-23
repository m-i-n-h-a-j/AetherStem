class TensorRTBackend:
    name = "tensorrt"

    def available(self) -> bool:
        return False

    def devices(self) -> list[str]:
        return []

    def select_device(self, preferred: str = "auto") -> str:
        raise RuntimeError("TensorRT backend is not implemented in AetherStem v0.3.")

    def memory_summary(self) -> dict[str, str]:
        return {"status": "unsupported"}

    def infer(self, callable_obj, *args, **kwargs):
        raise RuntimeError("TensorRT inference is not implemented in AetherStem v0.3.")

