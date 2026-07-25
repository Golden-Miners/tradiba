from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from uuid import UUID
from typing import Any

class ModelStatus(Enum):
    CANDIDATE = "CANDIDATE"
    VALIDATED = "VALIDATED"
    SHADOW = "SHADOW"
    PRODUCTION = "PRODUCTION"
    ARCHIVED = "ARCHIVED"

@dataclass
class RegisteredModel:
    model_id: UUID
    experiment_id: UUID
    status: ModelStatus = ModelStatus.CANDIDATE
    promoted_by: str | None = None
    promotion_time: datetime | None = None
    # Real implementation would have a storage path or artifact reference
    artifact_path: str = ""

class ModelRegistry:
    """
    Manages the lifecycle of trained models.
    """
    def __init__(self):
        self._models: dict[UUID, RegisteredModel] = {}

    def register(self, model: RegisteredModel) -> None:
        self._models[model.model_id] = model

    def promote(self, model_id: UUID, new_status: ModelStatus, promoted_by: str) -> None:
        model = self._models.get(model_id)
        if not model:
            raise ValueError(f"Model {model_id} not found")
        model.status = new_status
        model.promoted_by = promoted_by
        model.promotion_time = datetime.now()

    def archive(self, model_id: UUID) -> None:
        model = self._models.get(model_id)
        if model:
            model.status = ModelStatus.ARCHIVED

    def load(self, model_id: UUID) -> Any:
        """Loads a model artifact from storage."""
        # Stub implementation
        model = self._models.get(model_id)
        if not model:
            raise ValueError("Model not found")
        return f"Model_Artifact({model_id})"
