from tradiba.market.models import Candle

from .events import (
    BearishBOSEvent,
    BullishBOSEvent,
    TrendChangedEvent,
)
from .models import Trend
from .state import MarketStructureState


class BOSDetector:

    def __init__(self):
        self.state = MarketStructureState()

    def update_high(self, swing):
        self.state.last_swing_high = swing

    def update_low(self, swing):
        self.state.last_swing_low = swing

    def update_candle(self, candle: Candle):

        events = []

        if (
            self.state.last_swing_high
            and candle.close > self.state.last_swing_high.price
        ):
            if self.state.last_broken_high != self.state.last_swing_high.price:
                self.state.last_broken_high = self.state.last_swing_high.price

                events.append(
                    BullishBOSEvent(
                        candle=candle,
                        broken_price=self.state.last_swing_high.price,
                    )
                )

                if self.state.trend != Trend.BULLISH:
                    previous = self.state.trend
                    self.state.trend = Trend.BULLISH

                    events.append(
                        TrendChangedEvent(
                            previous=previous,
                            current=Trend.BULLISH,
                        )
                    )

        if (
            self.state.last_swing_low
            and candle.close < self.state.last_swing_low.price
        ):
            if self.state.last_broken_low != self.state.last_swing_low.price:
                self.state.last_broken_low = self.state.last_swing_low.price

                events.append(
                    BearishBOSEvent(
                        candle=candle,
                        broken_price=self.state.last_swing_low.price,
                    )
                )

                if self.state.trend != Trend.BEARISH:
                    previous = self.state.trend
                    self.state.trend = Trend.BEARISH

                    events.append(
                        TrendChangedEvent(
                            previous=previous,
                            current=Trend.BEARISH,
                        )
                    )

        return events
