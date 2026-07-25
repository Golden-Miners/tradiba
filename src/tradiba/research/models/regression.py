from tradiba.research.models.base import QuantitativeModel
from typing import Any
import json

class LinearRegressionModel(QuantitativeModel):
    """
    Stub for a regression model (e.g. N-bar return prediction).
    """
    def __init__(self):
        self.is_fitted = False
        
    def fit(self, features: Any, labels: Any) -> None:
        self.is_fitted = True

    def predict(self, features: Any) -> Any:
        if not self.is_fitted:
            raise ValueError("Model is not fitted")
        # Dummy prediction
        return 0.005

    def serialize(self) -> bytes:
        return json.dumps({"type": "LinearRegressionModel", "is_fitted": self.is_fitted}).encode("utf-8")

    @classmethod
    def deserialize(cls, data: bytes) -> 'LinearRegressionModel':
        state = json.loads(data.decode("utf-8"))
        model = cls()
        model.is_fitted = state["is_fitted"]
        return model
