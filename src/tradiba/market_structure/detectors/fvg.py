from typing import List
from tradiba.events import Event
from tradiba.mt5.models import Candle
from tradiba.market_structure.state import TimeframeState
from tradiba.market_structure.models import FairValueGap, Trend, ZoneStatus
from tradiba.market_structure.events import (
    FairValueGapCreatedEvent,
    FairValueGapFilledEvent,
    FairValueGapArchivedEvent,
)
from .base import Detector


class FVGDetector(Detector):
    """
    Detects Fair Value Gaps and manages their lifecycle.

    Zone lifecycle:
        OPEN → PARTIAL_FILL (price enters the gap)
        OPEN/PARTIAL_FILL → FILLED (price fills the entire gap)
        OPEN → ARCHIVED (gap is older than ``max_age`` candles)
    """

    def __init__(self, max_age: int = 50) -> None:
        self.max_age = max_age

    def update(self, candle: Candle, state: TimeframeState, current_events: List[Event]) -> List[Event]:
        events: List[Event] = []

        # 1. Lifecycle management of existing FVGs
        removed_fvgs: List[FairValueGap] = []
        for fvg in state.active_fvgs:
            # Check mitigation / partial fill
            if fvg.direction == Trend.BULLISH:
                if candle.low <= fvg.lower:
                    fvg.status = ZoneStatus.FILLED
                    removed_fvgs.append(fvg)
                    events.append(FairValueGapFilledEvent(
                        symbol=state.symbol, timeframe=state.timeframe, fvg=fvg,
                    ))
                elif candle.low <= fvg.upper:
                    fvg.status = ZoneStatus.PARTIAL_FILL
            elif fvg.direction == Trend.BEARISH:
                if candle.high >= fvg.upper:
                    fvg.status = ZoneStatus.FILLED
                    removed_fvgs.append(fvg)
                    events.append(FairValueGapFilledEvent(
                        symbol=state.symbol, timeframe=state.timeframe, fvg=fvg,
                    ))
                elif candle.high >= fvg.lower:
                    fvg.status = ZoneStatus.PARTIAL_FILL

            # Age-based invalidation
            if fvg not in removed_fvgs:
                age = state.candle_count - fvg.created_candle_count
                if age > self.max_age:
                    fvg.status = ZoneStatus.ARCHIVED
                    removed_fvgs.append(fvg)
                    events.append(FairValueGapArchivedEvent(
                        symbol=state.symbol, timeframe=state.timeframe, fvg=fvg,
                    ))

        for f in removed_fvgs:
            state.active_fvgs.remove(f)

        # 2. Detect new FVGs
        if len(state.candles) < 3:
            return events

        c1 = state.candles[-3]
        c3 = state.candles[-1]

        # Bullish FVG: gap between candle 1 high and candle 3 low
        if c1.high < c3.low:
            fvg = FairValueGap(
                upper=c3.low,
                lower=c1.high,
                direction=Trend.BULLISH,
                created_candle_count=state.candle_count,
                status=ZoneStatus.OPEN,
            )
            state.active_fvgs.append(fvg)
            events.append(FairValueGapCreatedEvent(
                symbol=candle.symbol, timeframe=candle.timeframe, fvg=fvg,
            ))

        # Bearish FVG: gap between candle 1 low and candle 3 high
        if c1.low > c3.high:
            fvg = FairValueGap(
                upper=c1.low,
                lower=c3.high,
                direction=Trend.BEARISH,
                created_candle_count=state.candle_count,
                status=ZoneStatus.OPEN,
            )
            state.active_fvgs.append(fvg)
            events.append(FairValueGapCreatedEvent(
                symbol=candle.symbol, timeframe=candle.timeframe, fvg=fvg,
            ))

        return events
