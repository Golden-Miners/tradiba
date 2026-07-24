from tradiba.risk.models import TradePlan
from tradiba.portfolio.aggregate import Portfolio
from .exceptions import ExecutionValidationFailed

class ExecutionValidator:
    def validate(
        self,
        trade_plan: TradePlan,
        portfolio: Portfolio,
    ) -> None:
        if trade_plan.position_size <= 0:
            raise ExecutionValidationFailed("Trade plan position size must be greater than zero")
