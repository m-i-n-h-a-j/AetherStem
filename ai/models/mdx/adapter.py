from ai.models._placeholder import StemPassthroughModel
from ai.models.metadata import ModelCapabilities, ModelMetadata, ModelRequirements


class MdxPlaceholderModel(StemPassthroughModel):
    metadata = ModelMetadata(
        name="mdx-placeholder",
        version="0.3.0",
        family="mdx",
        description="MDX/UVR-compatible ONNX placeholder adapter.",
        capabilities=ModelCapabilities(separate=True, stems=["vocals", "instrumental"]),
        requirements=ModelRequirements(backends=["onnx"], devices=["cpu", "cuda"], dependencies=["onnxruntime"]),
    )

