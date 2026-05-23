from ai.models._placeholder import PassthroughModel
from ai.models.metadata import ModelCapabilities, ModelMetadata, ModelRequirements


class EnhancementPlaceholderModel(PassthroughModel):
    metadata = ModelMetadata(
        name="enhancement-placeholder",
        version="0.3.0",
        family="enhancement",
        description="Validation-aware enhancement placeholder adapter.",
        capabilities=ModelCapabilities(enhance=True, bandwidth_extension=True),
        requirements=ModelRequirements(backends=["torch"], devices=["cpu", "cuda"]),
    )

