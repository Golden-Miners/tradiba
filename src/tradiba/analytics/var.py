from abc import ABC, abstractmethod
from typing import Any
from tradiba.analytics.portfolio import PortfolioSnapshot

class ValueAtRiskModel(ABC):
    """
    Base abstraction for computing Value at Risk (VaR).
    """
    @abstractmethod
    def calculate(self, snapshot: PortfolioSnapshot, confidence_level: float = 0.95, horizon_days: int = 1) -> dict[str, Any]:
        """
        Computes VaR metrics.
        Returns a dictionary containing the estimated maximum loss.
        """
        pass

class HistoricalVaR(ValueAtRiskModel):
    def calculate(self, snapshot: PortfolioSnapshot, confidence_level: float = 0.95, horizon_days: int = 1) -> dict[str, Any]:
        return {
            "method": "historical",
            "confidence_level": confidence_level,
            "horizon_days": horizon_days,
            "var_value": float(snapshot.equity) * 0.05 # Stub: 5% of equity
        }

class ParametricVaR(ValueAtRiskModel):
    def calculate(self, snapshot: PortfolioSnapshot, confidence_level: float = 0.95, horizon_days: int = 1) -> dict[str, Any]:
        return {
            "method": "parametric",
            "confidence_level": confidence_level,
            "horizon_days": horizon_days,
            "var_value": float(snapshot.equity) * 0.045
        }

class MonteCarloVaR(ValueAtRiskModel):
    def calculate(self, snapshot: PortfolioSnapshot, confidence_level: float = 0.95, horizon_days: int = 1) -> dict[str, Any]:
        return {
            "method": "monte_carlo",
            "confidence_level": confidence_level,
            "horizon_days": horizon_days,
            "var_value": float(snapshot.equity) * 0.055
        }
