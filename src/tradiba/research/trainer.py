from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID

class TrainingPipeline(ABC):
    """
    Base class for model training pipelines.
    Enforces a standard structure for training runs.
    """
    
    @abstractmethod
    def prepare_dataset(self, dataset_id: UUID) -> Any:
        """Loads and prepares the dataset for training."""
        pass

    @abstractmethod
    def train(self, data: Any, parameters: dict[str, Any]) -> Any:
        """Executes the training loop. Returns a model artifact."""
        pass

    @abstractmethod
    def evaluate(self, model: Any, data: Any) -> dict[str, float]:
        """Evaluates the model against hold-out/validation data."""
        pass

    @abstractmethod
    def register(self, experiment_id: UUID, model: Any, metrics: dict[str, float]) -> None:
        """Registers the completed model with the ModelRegistry."""
        pass
