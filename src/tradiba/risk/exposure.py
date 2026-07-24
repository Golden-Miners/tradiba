from tradiba.strategy.models import TradingSignal
from .models import PortfolioSnapshot

class ExposureManager:
    def current(self, account: PortfolioSnapshot):
        pass

    def can_open(self, signal: TradingSignal) -> bool:
        return True
