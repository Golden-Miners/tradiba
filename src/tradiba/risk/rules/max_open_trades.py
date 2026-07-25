from tradiba.strategy.models import TradingSignal
from tradiba.ports.execution import ExecutionProvider

from ..base import RiskRule
from ..models import TradePlan


class MaximumOpenTradesRule(RiskRule):

    def __init__(
        self,
        maximum: int,
        provider: ExecutionProvider,
    ):
        self.maximum = maximum
        self.provider = provider

    def validate(
        self,
        signal: TradingSignal,
    ) -> TradePlan:
        
        # We assume ExecutionProvider has a positions() method
        try:
            positions = self.provider.positions()
        except NotImplementedError:
            positions = []
            
        if len(positions) >= self.maximum:
            return TradePlan(
                False,
                f"Maximum open trades exceeded ({len(positions)} >= {self.maximum})",
            )

        return TradePlan(True)
