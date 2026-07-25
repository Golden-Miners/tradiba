from abc import ABC, abstractmethod
from tradiba.analytics.portfolio import PortfolioSnapshot

class RiskFactor(ABC):
    """
    Base abstraction for a risk factor (e.g., Equity Beta, Interest Rate).
    """
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the risk factor."""
        pass

    @abstractmethod
    def exposure(self, portfolio: PortfolioSnapshot) -> float:
        """
        Calculates the portfolio's exposure to this specific risk factor.
        """
        pass

class EquityBetaFactor(RiskFactor):
    @property
    def name(self) -> str:
        return "equity_beta"

    def exposure(self, portfolio: PortfolioSnapshot) -> float:
        return 1.2 # Stub calculation

class InterestRateFactor(RiskFactor):
    @property
    def name(self) -> str:
        return "interest_rate"

    def exposure(self, portfolio: PortfolioSnapshot) -> float:
        return -0.5 # Stub calculation
