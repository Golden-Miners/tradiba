from tradiba.market_structure.narrative import MarketNarrative
from .manager import StrategyManager
from .resolver import ConflictResolver
from .models import TradingSignal

class StrategyEngine:
    def __init__(
        self,
        manager: StrategyManager,
        resolver: ConflictResolver,
    ):
        self.manager = manager
        self.conflicts = resolver

    def process(
        self,
        narrative: MarketNarrative,
    ) -> list[TradingSignal]:
        signals = self.manager.evaluate(narrative)
        signals = self.conflicts.resolve(signals)
        signals.sort(key=lambda s: (s.symbol, s.timeframe, s.side.name, s.strategy))
        return signals
