from __future__ import annotations

from collections import deque

from tradiba.market.models import Candle

from .events import SwingHighEvent
from .events import SwingLowEvent
from .models import SwingPoint
from .models import SwingType


class SwingDetector:

    def __init__(self):

        self._candles = deque(maxlen=5)

    def update(
        self,
        candle: Candle,
    ):

        self._candles.append(candle)

        if len(self._candles) < 5:
            return None

        c0, c1, c2, c3, c4 = self._candles

        if (
            c2.high > c0.high
            and c2.high > c1.high
            and c2.high > c3.high
            and c2.high > c4.high
        ):

            return SwingHighEvent(
                SwingPoint(
                    symbol=c2.symbol,
                    timeframe=c2.timeframe.name,
                    type=SwingType.HIGH,
                    candle_time=c2.open_time,
                    price=c2.high,
                    candle=c2,
                )
            )

        if (
            c2.low < c0.low
            and c2.low < c1.low
            and c2.low < c3.low
            and c2.low < c4.low
        ):

            return SwingLowEvent(
                SwingPoint(
                    symbol=c2.symbol,
                    timeframe=c2.timeframe.name,
                    type=SwingType.LOW,
                    candle_time=c2.open_time,
                    price=c2.low,
                    candle=c2,
                )
            )

        return None
