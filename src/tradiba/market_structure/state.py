"""
Market structure analysis state.
"""

from __future__ import annotations

from collections import deque

from tradiba.mt5.models import Candle

from .models import SwingHigh, SwingLow, Trend

# Number of candles in the swing-detection window.
SWING_WINDOW = 5


class MarketStructureState:
    """
    Mutable analysis state for a single (symbol, timeframe) pair.

    Updated by :class:`MarketStructureService` as candles arrive.
    """

    __slots__ = (
        "symbol",
        "timeframe",
        "trend",
        "last_swing_high",
        "last_swing_low",
        "candles",
    )

    def __init__(self, symbol: str, timeframe: str) -> None:
        self.symbol = symbol
        self.timeframe = timeframe
        self.trend: Trend = Trend.NEUTRAL
        self.last_swing_high: SwingHigh | None = None
        self.last_swing_low: SwingLow | None = None
        self.candles: deque[Candle] = deque(maxlen=SWING_WINDOW)
