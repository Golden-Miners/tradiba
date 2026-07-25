from typing import Any
from tradiba.sdk_v2.strategy import Strategy
from tradiba.sdk_v2.context import StrategyContext

class StrategyHarness:
    """
    Local simulation harness for unit testing strategies.
    Allows feeding in data predictably and checking generated signals.
    """
    def __init__(self, strategy: Strategy) -> None:
        self.strategy = strategy
        self.ctx = StrategyContext()
        self.strategy._bind_context(self.ctx)
        self.strategy.on_initialize(self.ctx)
        self.strategy.on_start(self.ctx)
        self._signals: list[Any] = []

    def feed(self, event_name: str, data: Any) -> None:
        """Feed a mock event into the strategy."""
        # Find subscribed methods
        for attr_name in dir(self.strategy):
            attr = getattr(self.strategy, attr_name)
            if hasattr(attr, "_subscriptions"):
                if event_name in attr._subscriptions:
                    attr(data)

    def signals(self) -> list[Any]:
        """Return the signals generated during the simulation."""
        return self._signals
