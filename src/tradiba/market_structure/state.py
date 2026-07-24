"""
Market structure analysis state.
"""

from __future__ import annotations

from collections import deque
from typing import List, Optional

from tradiba.mt5.models import Candle
from .models import (
    Trend, SwingPoint, OrderBlock, FairValueGap, LiquidityPool,
    BreakOfStructure, ChangeOfCharacter,
)

class TimeframeState:
    """
    Mutable analysis state for a single timeframe.

    Every detector reads and writes to this shared state object.
    No detector should maintain isolated state.
    """
    __slots__ = (
        "symbol",
        "timeframe",
        "trend",
        "last_swing_high",
        "last_swing_low",
        "swings",
        "unmitigated_swing_highs",
        "unmitigated_swing_lows",
        "candles",
        "active_order_blocks",
        "active_fvgs",
        "liquidity_pools",
        "candle_count",
        "bos_history",
        "choch_history",
        "last_bos",
        "last_choch",
    )

    def __init__(self, symbol: str, timeframe: str) -> None:
        self.symbol = symbol
        self.timeframe = timeframe
        self.trend: Trend = Trend.NEUTRAL

        self.last_swing_high: Optional[SwingPoint] = None
        self.last_swing_low: Optional[SwingPoint] = None

        # Full swing history (capped for memory)
        self.swings: List[SwingPoint] = []

        self.unmitigated_swing_highs: List[SwingPoint] = []
        self.unmitigated_swing_lows: List[SwingPoint] = []

        # Keep enough history for swing detection and order blocks
        self.candles: deque[Candle] = deque(maxlen=100)

        self.active_order_blocks: List[OrderBlock] = []
        self.active_fvgs: List[FairValueGap] = []
        self.liquidity_pools: List[LiquidityPool] = []
        self.candle_count = 0

        # BOS / CHOCH audit trail
        self.bos_history: List[BreakOfStructure] = []
        self.choch_history: List[ChangeOfCharacter] = []
        self.last_bos: Optional[BreakOfStructure] = None
        self.last_choch: Optional[ChangeOfCharacter] = None


class MarketStructureState:
    """
    Mutable state for a symbol containing states for multiple timeframes.
    """
    __slots__ = (
        "symbol",
        "timeframes",
    )

    def __init__(self, symbol: str) -> None:
        self.symbol = symbol
        self.timeframes: dict[str, TimeframeState] = {}
        
    def get_timeframe_state(self, timeframe: str) -> TimeframeState:
        if timeframe not in self.timeframes:
            self.timeframes[timeframe] = TimeframeState(self.symbol, timeframe)
        return self.timeframes[timeframe]
