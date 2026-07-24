from __future__ import annotations

from datetime import datetime, timezone

from .events import CandleClosedEvent
from .models import Candle
from .models import Tick
from .models import Timeframe


class BarAggregator:

    def __init__(
        self,
        timeframe: Timeframe,
    ):

        self._timeframe = timeframe
        self._current: Candle | None = None

    def update(
        self,
        tick: Tick,
    ) -> CandleClosedEvent | None:

        bucket = self._bucket_start(tick.time)

        if self._current is None:

            self._current = Candle(
                symbol=tick.symbol,
                timeframe=self._timeframe,
                open_time=bucket,
                open=tick.bid,
                high=tick.bid,
                low=tick.bid,
                close=tick.bid,
                volume=tick.volume,
            )

            return None

        if bucket != self._current.open_time:

            finished = self._current

            self._current = Candle(
                symbol=tick.symbol,
                timeframe=self._timeframe,
                open_time=bucket,
                open=tick.bid,
                high=tick.bid,
                low=tick.bid,
                close=tick.bid,
                volume=tick.volume,
            )

            return CandleClosedEvent(
                candle=finished,
            )

        self._current.high = max(
            self._current.high,
            tick.bid,
        )

        self._current.low = min(
            self._current.low,
            tick.bid,
        )

        self._current.close = tick.bid

        self._current.volume += tick.volume

        return None

    def current(self) -> Candle | None:
        return self._current

    def _bucket_start(
        self,
        dt: datetime,
    ) -> datetime:

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)

        seconds = int(dt.timestamp())

        interval = self._timeframe.value

        start = seconds - (seconds % interval)

        return datetime.fromtimestamp(
            start,
            tz=timezone.utc,
        )
