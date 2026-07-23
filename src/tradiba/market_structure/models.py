"""
Market structure domain models.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from tradiba.mt5.models import Candle


class Trend(Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"


@dataclass(frozen=True, slots=True)
class SwingHigh:
    """A confirmed swing high point in price action."""

    candle: Candle
    price: float  # candle.high


@dataclass(frozen=True, slots=True)
class SwingLow:
    """A confirmed swing low point in price action."""

    candle: Candle
    price: float  # candle.low


@dataclass(frozen=True, slots=True)
class BreakOfStructure:
    """Price broke a swing level in the direction of the current trend."""

    candle: Candle
    broken_level: float
    direction: Trend  # BULLISH or BEARISH


@dataclass(frozen=True, slots=True)
class ChangeOfCharacter:
    """Price broke a swing level against the current trend (potential reversal)."""

    candle: Candle
    broken_level: float
    direction: Trend  # the NEW trend direction
