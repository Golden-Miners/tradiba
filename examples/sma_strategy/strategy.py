from tradiba.sdk.strategy import StrategyPlugin
from tradiba.market_structure.narrative import MarketNarrative
from tradiba.strategy.models import TradingSignal
from tradiba.sdk.events import subscribe
from tradiba.strategy.events import StrategyConfiguredEvent

class SmaCrossoverStrategy(StrategyPlugin):
    def __init__(self):
        super().__init__(name="sma_crossover", priority=50)

    def initialize(self, context):
        context.logger.info("SMA Crossover Strategy initialized")

    def evaluate(self, narrative: MarketNarrative) -> list[TradingSignal]:
        # Simple dummy logic for demonstration
        return []

    @subscribe(StrategyConfiguredEvent)
    def on_configured(self, event: StrategyConfiguredEvent):
        pass
