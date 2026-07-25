from abc import ABC, abstractmethod
from typing import Any
from tradiba.analytics.portfolio import PortfolioSnapshot

class PortfolioOptimizer(ABC):
    """
    Produces target allocations based on a specific optimization objective.
    """
    @abstractmethod
    def optimize(self, snapshot: PortfolioSnapshot, constraints: dict[str, Any]) -> dict[str, float]:
        """
        Returns a dictionary mapping asset/strategy to target weight (0.0 to 1.0).
        """
        pass

class MaxSharpeOptimizer(PortfolioOptimizer):
    def optimize(self, snapshot: PortfolioSnapshot, constraints: dict[str, Any]) -> dict[str, float]:
        # Stub logic
        return {"strategy_1": 0.6, "strategy_2": 0.4}

class RiskParityOptimizer(PortfolioOptimizer):
    def optimize(self, snapshot: PortfolioSnapshot, constraints: dict[str, Any]) -> dict[str, float]:
        # Stub logic
        return {"strategy_1": 0.5, "strategy_2": 0.5}
