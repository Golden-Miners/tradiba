from abc import ABC, abstractmethod
from typing import Any

class ValidationStrategy(ABC):
    """
    Base class for model validation techniques 
    (e.g., HoldOut, WalkForward, CrossValidation).
    """
    
    @abstractmethod
    def validate(self, model: Any, data: Any) -> dict[str, float]:
        """
        Validates the model against the provided dataset.
        Returns a dictionary of metrics.
        """
        pass

class WalkForwardValidation(ValidationStrategy):
    """
    Walk-forward optimization/validation to prevent look-ahead bias
    in time series models.
    """
    def __init__(self, window_size: int, step_size: int):
        self.window_size = window_size
        self.step_size = step_size
        
    def validate(self, model: Any, data: Any) -> dict[str, float]:
        # Stub implementation
        return {"sharpe": 1.5, "max_drawdown": 0.15}
