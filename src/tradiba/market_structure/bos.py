from tradiba.market.models import Candle

from .events import (
    BearishBOSEvent,
    BullishBOSEvent,
    TrendChangedEvent,
)
from .models import Trend
from .state import MarketStructureState


class BOSDetector:

    def update_candle(
        self,
        candle: Candle,
        state: MarketStructureState,
    ):
        events = []

        if (
            state.last_swing_high
            and candle.close > state.last_swing_high.price
        ):
            if state.last_broken_high != state.last_swing_high.price:
                events.append(
                    BullishBOSEvent(
                        candle=candle,
                        broken_price=state.last_swing_high.price,
                    )
                )

                if state.trend != Trend.BULLISH:
                    events.append(
                        TrendChangedEvent(
                            previous=state.trend,
                            current=Trend.BULLISH,
                        )
                    )

        if (
            state.last_swing_low
            and candle.close < state.last_swing_low.price
        ):
            if state.last_broken_low != state.last_swing_low.price:
                events.append(
                    BearishBOSEvent(
                        candle=candle,
                        broken_price=state.last_swing_low.price,
                    )
                )

                if state.trend != Trend.BEARISH:
                    events.append(
                        TrendChangedEvent(
                            previous=state.trend,
                            current=Trend.BEARISH,
                        )
                    )

        return events
