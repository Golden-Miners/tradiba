from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime


@dataclass(slots=True, frozen=True)
class AccountSnapshot:
    timestamp: datetime

    balance: Decimal
    equity: Decimal
    margin: Decimal
    free_margin: Decimal
    margin_level: Decimal

    floating_profit: Decimal
    realized_profit: Decimal
