from tradiba.research.models.base import QuantitativeModel
from typing import Any
import json

class BinaryClassifierModel(QuantitativeModel):
    """
    Stub for a binary classification model (e.g. up/down prediction).
    """
    def __init__(self):
        self.is_fitted = False
        
    def fit(self, features: Any, labels: Any) -> None:
        self.is_fitted = True

    def predict(self, features: Any) -> Any:
        if not self.is_fitted:
            raise ValueError("Model is not fitted")
        # Dummy prediction
        return 1

    def serialize(self) -> bytes:
        return json.dumps({"type": "BinaryClassifierModel", "is_fitted": self.is_fitted}).encode("utf-8")

    @classmethod
    def deserialize(cls, data: bytes) -> 'BinaryClassifierModel':
        state = json.loads(data.decode("utf-8"))
        model = cls()
        model.is_fitted = state["is_fitted"]
        return model
