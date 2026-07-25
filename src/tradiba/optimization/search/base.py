from abc import ABC, abstractmethod
from typing import Dict, Iterator, List

from ..configuration import Parameter


class SearchAlgorithm(ABC):
    """Base interface for search algorithms."""

    def __init__(self, parameters: List[Parameter]):
        self.parameters = parameters

    @abstractmethod
    def generate(self) -> Iterator[Dict[str, float]]:
        """Yields parameter sets for evaluation."""
        pass
