from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Timeframe(Enum):
    M1 = 60
    M5 = 300
    M15 = 900
    M30 = 1800
    H1 = 3600
    H4 = 14400
    D1 = 86400


@dataclass(slots=True, frozen=True)
class Tick:
    symbol: str
    bid: float
    ask: float
    time: datetime
    volume: int = 0


@dataclass(slots=True)
class Candle:
    symbol: str
    timeframe: Timeframe

    open_time: datetime

    open: float
    high: float
    low: float
    close: float

    volume: int = 0
