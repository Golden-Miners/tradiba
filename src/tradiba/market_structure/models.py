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


class Trend(Enum):
    UNKNOWN = "UNKNOWN"
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    RANGE = "RANGE"


class LiquidityType(Enum):
    BUY_SIDE = "BUY_SIDE"
    SELL_SIDE = "SELL_SIDE"


class LiquidityStatus(Enum):
    ACTIVE = "ACTIVE"
    SWEPT = "SWEPT"
    INVALIDATED = "INVALIDATED"


@dataclass(slots=True)
class LiquidityPool:
    id: str
    symbol: str
    timeframe: str
    price: float
    liquidity_type: LiquidityType
    touches: int
    tolerance: float
    created_at: datetime
    status: LiquidityStatus = LiquidityStatus.ACTIVE


class OrderBlockDirection(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"


class OrderBlockStatus(Enum):
    ACTIVE = "ACTIVE"
    TOUCHED = "TOUCHED"
    MITIGATED = "MITIGATED"
    INVALIDATED = "INVALIDATED"


@dataclass(slots=True)
class OrderBlock:
    id: str
    symbol: str
    timeframe: str
    direction: OrderBlockDirection
    high: float
    low: float
    origin_bos_price: float
    created_at: datetime
    status: OrderBlockStatus = OrderBlockStatus.ACTIVE
