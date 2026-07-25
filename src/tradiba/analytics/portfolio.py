from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass(slots=True, frozen=True)
class PortfolioSnapshot:
    """
    Immutable snapshot of a portfolio's state at a specific point in time,
    used as the primary input for all analytics calculations.
    """
    timestamp: datetime
    equity: Decimal
    cash: Decimal
    positions: tuple
    accounts: tuple
    currency: str
