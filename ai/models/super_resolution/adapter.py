from ai.models._placeholder import PassthroughModel
from ai.models.metadata import ModelCapabilities, ModelMetadata, ModelRequirements


class SuperResolutionPlaceholderModel(PassthroughModel):
    metadata = ModelMetadata(
        name="super-resolution-placeholder",
        version="0.3.0",
        family="super_resolution",
        description="Audio super-resolution placeholder adapter.",
        capabilities=ModelCapabilities(super_resolution=True, bandwidth_extension=True),
        requirements=ModelRequirements(backends=["torch"], devices=["cpu", "cuda"]),
    )

