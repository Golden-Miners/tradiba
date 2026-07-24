from abc import ABC, abstractmethod
from .aggregate import Portfolio

class PortfolioRepository(ABC):
    @abstractmethod
    def save(self, portfolio: Portfolio):
        pass

    @abstractmethod
    def load(self) -> Portfolio | None:
        pass
