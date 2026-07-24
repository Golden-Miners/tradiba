from tradiba.strategy.models import Signal
from tradiba.ports.execution import ExecutionProvider

from ..base import RiskRule
from ..models.risk_result import RiskResult


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
        signal: Signal,
    ) -> RiskResult:
        
        # We assume ExecutionProvider has a positions() method
        try:
            positions = self.provider.positions()
        except NotImplementedError:
            positions = []
            
        if len(positions) >= self.maximum:
            return RiskResult(
                False,
                f"Maximum open trades exceeded ({len(positions)} >= {self.maximum})",
            )

        return RiskResult(True)
