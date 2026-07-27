from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Candle:
    symbol: str
    timeframe: str
    timestamp: datetime

    open: float
    high: float
    low: float
    close: float

    tick_volume: int
    spread: int
    real_volume: int


@dataclass(frozen=True, slots=True)
class Tick:
    symbol: str
    timestamp: datetime
    bid: float
    ask: float
    last: float
    volume: int