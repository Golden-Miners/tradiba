from tradiba.strategy.models import Signal

from ..base import RiskRule
from ..models.risk_result import RiskResult


class DailyLossRule(RiskRule):

    def validate(
        self,
        signal: Signal,
    ) -> RiskResult:
        # Implementation comes later after persistence exists.
        return RiskResult(True)
