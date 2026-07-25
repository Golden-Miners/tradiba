from tradiba.strategy.models import TradingSignal

from ..base import RiskRule
from ..models import TradePlan


class DailyLossRule(RiskRule):

    def validate(
        self,
        signal: TradingSignal,
    ) -> TradePlan:
        # Implementation comes later after persistence exists.
        return TradePlan(True)
