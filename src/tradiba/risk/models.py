from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from enum import Enum


class RiskDecision(Enum):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    REDUCED = "REDUCED"


@dataclass(slots=True, frozen=True)
class TradePlan:
    signal_id: str
    symbol: str
    side: str

    entry: Decimal
    stop_loss: Decimal
    take_profit: Decimal

    position_size: Decimal
    risk_amount: Decimal

    decision: RiskDecision

    reason: str | None = None

@dataclass(slots=True, frozen=True)
class PortfolioSnapshot:
    equity: Decimal
    balance: Decimal
    floating_pnl: Decimal
    daily_pnl: Decimal
    open_positions: int
    open_orders: int
