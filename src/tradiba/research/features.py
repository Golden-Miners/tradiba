from abc import ABC, abstractmethod
from typing import Any

class Feature(ABC):
    """
    Base class for all quantitative features.
    Features should be deterministic and composable.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the feature (e.g. 'ATR_14')."""
        pass

    @abstractmethod
    def compute(self, data: Any) -> Any:
        """
        Compute the feature given a window of data.
        In a real implementation, data is likely a Pandas DataFrame or Numpy array.
        """
        pass

class Label(ABC):
    """
    Base class for training labels.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def generate(self, data: Any) -> Any:
        pass
