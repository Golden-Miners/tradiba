from abc import ABC, abstractmethod
from tradiba.strategy.models import TradingSignal
from .models import PortfolioSnapshot

class RiskRule(ABC):

    @abstractmethod
    def evaluate(
        self,
        signal: TradingSignal,
        account: PortfolioSnapshot,
        exposure,
    ) -> bool:
        pass
