from tradiba.market_structure.narrative import MarketNarrative
from .registry import StrategyRegistry
from .validator import SignalValidator
from .models import TradingSignal

class StrategyManager:

    def __init__(
        self,
        registry: StrategyRegistry,
        validator: SignalValidator,
    ):

        self.registry = registry
        self.validator = validator

    def evaluate(
        self,
        narrative: MarketNarrative,
    ) -> list[TradingSignal]:

        signals = []

        for strategy in self.registry.strategies():

            produced = strategy.evaluate(narrative)

            for signal in produced:

                if self.validator.validate(signal):

                    signals.append(signal)

        return signals
