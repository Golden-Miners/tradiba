from tradiba.strategy.models import TradingSignal

from ..base import RiskRule
from ..models import TradePlan


class MaximumPositionSizeRule(RiskRule):

    def __init__(
        self,
        maximum: float,
    ):
        self.maximum = maximum

    def validate(
        self,
        signal: TradingSignal,
    ) -> TradePlan:

        if signal.volume > self.maximum:
            return TradePlan(
                False,
                "Maximum position exceeded",
            )

        return TradePlan(True)
