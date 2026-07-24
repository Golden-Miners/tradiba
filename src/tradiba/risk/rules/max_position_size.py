from tradiba.strategy.models import Signal

from ..base import RiskRule
from ..models.risk_result import RiskResult


class MaximumPositionSizeRule(RiskRule):

    def __init__(
        self,
        maximum: float,
    ):
        self.maximum = maximum

    def validate(
        self,
        signal: Signal,
    ) -> RiskResult:

        if signal.volume > self.maximum:
            return RiskResult(
                False,
                "Maximum position exceeded",
            )

        return RiskResult(True)
