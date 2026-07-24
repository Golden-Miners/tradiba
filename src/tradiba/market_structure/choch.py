from tradiba.market.models import Candle

from .events import (
    BullishCHOCHEvent,
    BearishCHOCHEvent,
)
from .models import Trend
from .state import MarketStructureState


class CHOCHDetector:

    def update(
        self,
        candle: Candle,
        state: MarketStructureState,
    ):

        events = []

        if (
            state.trend == Trend.BULLISH
            and state.last_swing_low
            and candle.close < state.last_swing_low.price
            and not state.choch_detected
        ):

            events.append(
                BearishCHOCHEvent(
                    candle=candle,
                    broken_price=state.last_swing_low.price,
                )
            )

        elif (
            state.trend == Trend.BEARISH
            and state.last_swing_high
            and candle.close > state.last_swing_high.price
            and not state.choch_detected
        ):

            events.append(
                BullishCHOCHEvent(
                    candle=candle,
                    broken_price=state.last_swing_high.price,
                )
            )

        return events
