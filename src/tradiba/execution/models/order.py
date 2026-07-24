from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class OrderSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"
    STOP = "STOP"


@dataclass(slots=True, frozen=True)
class Order:
    id: str
    symbol: str
    side: OrderSide
    order_type: OrderType
    volume: float
    price: float
    stop_loss: float
    take_profit: float
    created_at: datetime
