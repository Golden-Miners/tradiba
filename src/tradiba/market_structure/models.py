"""
Market structure domain models.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from datetime import datetime

from tradiba.mt5.models import Candle


class Trend(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    RANGE = "RANGE"
    NEUTRAL = "NEUTRAL"


class SwingKind(Enum):
    HIGH = auto()
    LOW = auto()


class ZoneStatus(Enum):
    OPEN = "OPEN"
    PARTIAL_FILL = "PARTIAL_FILL"
    FILLED = "FILLED"
    ARCHIVED = "ARCHIVED"


@dataclass(slots=True, frozen=True)
class SwingPoint:
    """A confirmed swing point (high or low) in price action."""
    index: int
    timestamp: datetime
    price: float
    kind: SwingKind
    candle: Candle


@dataclass(frozen=True, slots=True)
class BreakOfStructure:
    """Price broke a swing level in the direction of the current trend."""
    candle: Candle
    broken_price: float
    direction: Trend  # BULLISH or BEARISH


@dataclass(frozen=True, slots=True)
class ChangeOfCharacter:
    """Price broke a swing level against the current trend (potential reversal)."""
    candle: Candle
    broken_price: float
    direction: Trend  # the NEW trend direction


@dataclass(slots=True)
class LiquidityPool:
    price: float
    strength: int
    direction: Trend
    created_at: datetime
    status: ZoneStatus = ZoneStatus.OPEN


@dataclass(slots=True)
class FairValueGap:
    upper: float
    lower: float
    direction: Trend
    created_candle_count: int = 0
    status: ZoneStatus = ZoneStatus.OPEN


@dataclass(slots=True)
class OrderBlock:
    zone_high: float
    zone_low: float
    direction: Trend
    created_at: datetime
    status: ZoneStatus
    originating_bos: BreakOfStructure
    created_candle_count: int = 0
