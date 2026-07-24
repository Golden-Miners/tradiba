from typing import List
from tradiba.events import Event
from tradiba.mt5.models import Candle
from tradiba.market_structure.state import TimeframeState
from tradiba.market_structure.models import SwingPoint, SwingKind
from tradiba.market_structure.events import SwingHighEvent, SwingLowEvent
from .base import Detector

class SwingDetector(Detector):
    def __init__(self, left_bars: int = 2, right_bars: int = 2):
        self.left_bars = left_bars
        self.right_bars = right_bars
        self.window_size = left_bars + right_bars + 1

    def update(self, candle: Candle, state: TimeframeState, current_events: List[Event]) -> List[Event]:
        events = []
        if len(state.candles) < self.window_size:
            return events

        # The candidate is the candle that is 'right_bars' back from the newest
        candidate_idx = len(state.candles) - self.right_bars - 1
        candidate = state.candles[candidate_idx]
        
        # Check swing high
        is_high = True
        for i in range(candidate_idx - self.left_bars, candidate_idx + self.right_bars + 1):
            if i == candidate_idx:
                continue
            if state.candles[i].high >= candidate.high:
                is_high = False
                break
                
        if is_high:
            sp = SwingPoint(
                index=state.candle_count - self.right_bars - 1,
                timestamp=candidate.timestamp,
                price=candidate.high,
                kind=SwingKind.HIGH,
                candle=candidate
            )
            state.last_swing_high = sp
            state.swings.append(sp)
            state.unmitigated_swing_highs.append(sp)
            events.append(SwingHighEvent(swing=sp))

        # Check swing low
        is_low = True
        for i in range(candidate_idx - self.left_bars, candidate_idx + self.right_bars + 1):
            if i == candidate_idx:
                continue
            if state.candles[i].low <= candidate.low:
                is_low = False
                break

        if is_low:
            sp = SwingPoint(
                index=state.candle_count - self.right_bars - 1,
                timestamp=candidate.timestamp,
                price=candidate.low,
                kind=SwingKind.LOW,
                candle=candidate
            )
            state.last_swing_low = sp
            state.swings.append(sp)
            state.unmitigated_swing_lows.append(sp)
            events.append(SwingLowEvent(swing=sp))

        return events
