from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SignalSide(Enum):
    BUY = "BUY"
    SELL = "SELL"


class SignalStrength(Enum):
    WEAK = 1
    NORMAL = 2
    STRONG = 3
    VERY_STRONG = 4


@dataclass(slots=True, frozen=True)
class TradingSignal:

    strategy: str

    symbol: str

    timeframe: str

    side: SignalSide

    strength: SignalStrength

    confidence: int

    entry: float

    stop_loss: float

    take_profit: float

    created_at: datetime

    metadata: dict[str, object]
