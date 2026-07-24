from tradiba.strategy.models import Signal
from tradiba.ports.execution import ExecutionProvider

from ..base import RiskRule
from ..models.risk_result import RiskResult


class MaximumSymbolExposureRule(RiskRule):

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
        
        try:
            positions = self.provider.positions()
        except NotImplementedError:
            positions = []
            
        symbol_positions = [p for p in positions if p.symbol == signal.symbol]
            
        if len(symbol_positions) >= self.maximum:
            return RiskResult(
                False,
                f"Maximum symbol exposure exceeded for {signal.symbol} ({len(symbol_positions)} >= {self.maximum})",
            )

        return RiskResult(True)
