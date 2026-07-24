from dataclasses import dataclass
from decimal import Decimal

@dataclass(slots=True, frozen=True)
class RiskLimits:
    account_risk_percent: Decimal
    daily_loss_percent: Decimal
    weekly_loss_percent: Decimal
    max_open_positions: int
    max_symbol_positions: int
    max_correlated_positions: int
