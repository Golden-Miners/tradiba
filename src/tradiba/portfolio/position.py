from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from enum import Enum


class PositionStatus(Enum):
    OPEN = "OPEN"
    CLOSED = "CLOSED"


@dataclass(slots=True)
class Position:
    ticket: int
    symbol: str
    volume: Decimal
    entry_price: Decimal
    current_price: Decimal
    stop_loss: Decimal
    take_profit: Decimal
    open_time: datetime
    profit: Decimal
    status: PositionStatus
