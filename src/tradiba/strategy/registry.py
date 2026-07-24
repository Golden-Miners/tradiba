from .interface import Strategy
from .exceptions import StrategyRegistrationError

class StrategyRegistry:

    def __init__(self):

        self._strategies = {}

    def register(self, strategy: Strategy):

        if strategy.name in self._strategies:
            raise StrategyRegistrationError(
                f"Duplicate strategy '{strategy.name}'"
            )

        self._strategies[strategy.name] = strategy

    def strategies(self):

        return sorted(
            (
                s
                for s in self._strategies.values()
                if s.enabled
            ),
            key=lambda s: s.priority,
        )
