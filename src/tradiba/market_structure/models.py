from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from tradiba.market.models import Candle


class SwingType(Enum):
    HIGH = "HIGH"
    LOW = "LOW"


@dataclass(slots=True, frozen=True)
class SwingPoint:
    symbol: str
    timeframe: str

    type: SwingType

    candle_time: datetime

    price: float

    candle: Candle
