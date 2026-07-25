from abc import ABC, abstractmethod
from typing import Any

class QuantitativeModel(ABC):
    """
    Base interface for all quantitative research models.
    """
    
    @abstractmethod
    def fit(self, features: Any, labels: Any) -> None:
        """Trains the model on historical features and labels."""
        pass

    @abstractmethod
    def predict(self, features: Any) -> Any:
        """Generates predictions from live or historical features."""
        pass

    @abstractmethod
    def serialize(self) -> bytes:
        """Serializes the model state for persistence."""
        pass

    @classmethod
    @abstractmethod
    def deserialize(cls, data: bytes) -> 'QuantitativeModel':
        """Reconstructs the model from persisted bytes."""
        pass
