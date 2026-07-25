from tradiba.research.models.base import QuantitativeModel
from typing import Any
import json

class ProbabilisticModel(QuantitativeModel):
    """
    Stub for a model that outputs probability distributions.
    """
    def __init__(self):
        self.is_fitted = False
        
    def fit(self, features: Any, labels: Any) -> None:
        self.is_fitted = True

    def predict(self, features: Any) -> Any:
        if not self.is_fitted:
            raise ValueError("Model is not fitted")
        # Dummy prediction (mean, std)
        return (0.0, 1.0)

    def serialize(self) -> bytes:
        return json.dumps({"type": "ProbabilisticModel", "is_fitted": self.is_fitted}).encode("utf-8")

    @classmethod
    def deserialize(cls, data: bytes) -> 'ProbabilisticModel':
        state = json.loads(data.decode("utf-8"))
        model = cls()
        model.is_fitted = state["is_fitted"]
        return model
