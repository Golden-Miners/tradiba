from abc import ABC, abstractmethod
from tradiba.analytics.portfolio import PortfolioSnapshot
from dataclasses import replace
from decimal import Decimal

class StressScenario(ABC):
    """
    Base abstraction for deterministic market shock scenarios.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def apply(self, snapshot: PortfolioSnapshot) -> PortfolioSnapshot:
        """
        Applies the stress scenario and returns a new (simulated) PortfolioSnapshot.
        """
        pass

class EquityMarketShock(StressScenario):
    @property
    def name(self) -> str:
        return "equity_market_minus_20_percent"

    def apply(self, snapshot: PortfolioSnapshot) -> PortfolioSnapshot:
        # Stub logic: just reduces equity by 20%
        shocked_equity = snapshot.equity * Decimal("0.80")
        return replace(snapshot, equity=shocked_equity)
