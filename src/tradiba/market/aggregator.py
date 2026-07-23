"""
Bar aggregator — builds candles from incoming ticks.

Subscribes to :class:`TickReceivedEvent` and emits
:class:`CandleClosedEvent` whenever a timeframe boundary is crossed.
"""

from __future__ import annotations

from datetime import datetime, timedelta

from tradiba.events import EventBus
from tradiba.logging import get_logger
from tradiba.mt5.models import Candle, Tick
from tradiba.mt5.timeframes import Timeframe

from .events import CandleClosedEvent, TickReceivedEvent

logger = get_logger(__name__)


# ------------------------------------------------------------------
# Timeframe boundary helpers
# ------------------------------------------------------------------

def _bar_open_time(timestamp: datetime, timeframe: Timeframe) -> datetime:
    """Return the start of the bar that contains *timestamp*."""
    if timeframe == Timeframe.M1:
        return timestamp.replace(second=0, microsecond=0)

    if timeframe == Timeframe.M5:
        m = timestamp.minute - timestamp.minute % 5
        return timestamp.replace(minute=m, second=0, microsecond=0)

    if timeframe == Timeframe.M15:
        m = timestamp.minute - timestamp.minute % 15
        return timestamp.replace(minute=m, second=0, microsecond=0)

    if timeframe == Timeframe.M30:
        m = timestamp.minute - timestamp.minute % 30
        return timestamp.replace(minute=m, second=0, microsecond=0)

    if timeframe == Timeframe.H1:
        return timestamp.replace(minute=0, second=0, microsecond=0)

    if timeframe == Timeframe.H4:
        h = timestamp.hour - timestamp.hour % 4
        return timestamp.replace(hour=h, minute=0, second=0, microsecond=0)

    if timeframe == Timeframe.D1:
        return timestamp.replace(hour=0, minute=0, second=0, microsecond=0)

    if timeframe == Timeframe.W1:
        days_since_monday = timestamp.weekday()  # Monday = 0
        monday = timestamp - timedelta(days=days_since_monday)
        return monday.replace(hour=0, minute=0, second=0, microsecond=0)

    if timeframe == Timeframe.MN1:
        return timestamp.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    raise ValueError(f"Unsupported timeframe: {timeframe}")


# ------------------------------------------------------------------
# Internal bar builder
# ------------------------------------------------------------------

class _BarBuilder:
    """Accumulates ticks into a single bar for one (symbol, timeframe)."""

    __slots__ = (
        "symbol",
        "timeframe",
        "open_time",
        "_open",
        "_high",
        "_low",
        "_close",
        "_tick_count",
        "_volume",
    )

    def __init__(self, symbol: str, timeframe: Timeframe) -> None:
        self.symbol = symbol
        self.timeframe = timeframe
        self.open_time: datetime | None = None
        self._open = 0.0
        self._high = 0.0
        self._low = 0.0
        self._close = 0.0
        self._tick_count = 0
        self._volume = 0

    def update(self, tick: Tick) -> Candle | None:
        """Feed a tick.  Returns a closed :class:`Candle` if a bar completed."""
        bar_time = _bar_open_time(tick.timestamp, self.timeframe)
        price = tick.bid

        if self.open_time is None:
            self._reset(bar_time, price, tick.volume)
            return None

        if bar_time == self.open_time:
            self._accumulate(price, tick.volume)
            return None

        # Timeframe boundary crossed — close the previous bar.
        closed = self._close_bar()
        self._reset(bar_time, price, tick.volume)
        return closed

    # --  private  -------------------------------------------------

    def _reset(self, bar_time: datetime, price: float, volume: int) -> None:
        self.open_time = bar_time
        self._open = price
        self._high = price
        self._low = price
        self._close = price
        self._tick_count = 1
        self._volume = volume

    def _accumulate(self, price: float, volume: int) -> None:
        if price > self._high:
            self._high = price
        if price < self._low:
            self._low = price
        self._close = price
        self._tick_count += 1
        self._volume += volume

    def _close_bar(self) -> Candle:
        assert self.open_time is not None
        return Candle(
            symbol=self.symbol,
            timeframe=self.timeframe.name,
            timestamp=self.open_time,
            open=self._open,
            high=self._high,
            low=self._low,
            close=self._close,
            tick_volume=self._tick_count,
            spread=0,
            real_volume=self._volume,
        )


# ------------------------------------------------------------------
# Public aggregator
# ------------------------------------------------------------------

class BarAggregator:
    """
    Converts a tick stream into candle bars.

    Subscribes to :class:`TickReceivedEvent` on the event bus.
    For each registered ``(symbol, timeframe)`` pair, maintains a
    :class:`_BarBuilder`.  When a timeframe boundary is crossed,
    publishes :class:`CandleClosedEvent`.
    """

    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self._builders: dict[tuple[str, str], _BarBuilder] = {}
        self._event_bus.subscribe(TickReceivedEvent, self._on_tick)

    def add_subscription(self, symbol: str, timeframe: Timeframe) -> None:
        key = (symbol, timeframe.name)
        if key not in self._builders:
            self._builders[key] = _BarBuilder(symbol, timeframe)
            logger.info("Aggregator tracking %s %s", symbol, timeframe.name)

    def remove_subscription(self, symbol: str) -> None:
        to_remove = [k for k in self._builders if k[0] == symbol]
        for key in to_remove:
            del self._builders[key]

    def clear(self) -> None:
        self._builders.clear()

    # --  event handler  -------------------------------------------

    def _on_tick(self, event: TickReceivedEvent) -> None:
        tick = event.tick
        for key, builder in self._builders.items():
            if key[0] != tick.symbol:
                continue

            closed = builder.update(tick)
            if closed is not None:
                self._event_bus.publish(CandleClosedEvent(candle=closed))
