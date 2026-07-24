"""
Market data service.

Manages symbol subscriptions, polls MT5 for live ticks, publishes
domain events, and coordinates bar aggregation.
"""

from __future__ import annotations

from tradiba.core.service import Service
from tradiba.events import EventBus
from tradiba.logging import get_logger
from tradiba.market.models import Tick, Timeframe
from tradiba.scheduler import Scheduler, Task
import threading
from datetime import timedelta

from .aggregator import BarAggregator
from .events import (
    SymbolConnectedEvent,
    SymbolDisconnectedEvent,
    TickEvent,
    CandleClosedEvent,
)
from tradiba.ports.market_data import MarketDataProvider
from .subscriptions import Subscription

logger = get_logger(__name__)

DEFAULT_POLL_INTERVAL: float = 0.2  # seconds


class MarketDataService(Service):
    """
    Polls MT5 for live ticks and publishes market data events.

    Use :meth:`subscribe` / :meth:`unsubscribe` to control which
    symbols are actively polled. Each new tick is deduplicated
    before being published as a :class:`TickEvent`.
    The internal :class:`BarAggregator` converts ticks into
    candles and emits :class:`CandleClosedEvent`.
    """

    def __init__(
        self,
        provider: MarketDataProvider,
        event_bus: EventBus,
        scheduler: Scheduler,
        poll_interval: float = DEFAULT_POLL_INTERVAL,
    ) -> None:
        self._provider = provider
        self._event_bus = event_bus
        self._scheduler = scheduler
        self._poll_interval = poll_interval

        self._subscriptions: dict[str, Subscription] = {}
        self._last_ticks: dict[str, Tick] = {}
        self._aggregators: dict[tuple[str, Timeframe], BarAggregator] = {}
        self._task_name = "market_data_poll"

    # ------------------------------------------------------------------
    # Subscription management
    # ------------------------------------------------------------------

    def subscribe(
        self,
        symbol: str,
        timeframe: Timeframe = Timeframe.M1,
    ) -> None:
        """Start monitoring *symbol* and building bars at *timeframe*."""
        if symbol in self._subscriptions:
            logger.warning("Already subscribed to %s", symbol)
            return

        sub = Subscription(symbol=symbol, timeframe=timeframe)
        self._subscriptions[symbol] = sub
        
        # Initialize the BarAggregator for this symbol/timeframe
        self._aggregators[(symbol, timeframe)] = BarAggregator(timeframe=timeframe)

        self._event_bus.publish(SymbolConnectedEvent(symbol=symbol))
        logger.info("Subscribed to %s (%s). Starting historical preload...", symbol, timeframe.name)
        threading.Thread(target=self._preload_history, args=(symbol, timeframe), daemon=True).start()

    def _preload_history(self, symbol: str, timeframe: Timeframe) -> None:
        """Asynchronously fetches historical candles and primes the aggregator/state."""
        try:
            # Preload last 500 candles to establish solid market structure state
            candles = self._provider.get_recent_candles(symbol, timeframe, 500)
            for candle in candles:
                self._event_bus.publish(CandleClosedEvent(candle=candle))
            logger.info("Historical preload completed for %s (%s), %d candles loaded.", symbol, timeframe.name, len(candles))
        except Exception:
            logger.exception("Failed to preload history for %s", symbol)

    def unsubscribe(self, symbol: str) -> None:
        """Stop monitoring *symbol*."""
        if symbol not in self._subscriptions:
            logger.warning("Not subscribed to %s", symbol)
            return

        sub = self._subscriptions[symbol]
        del self._subscriptions[symbol]
        self._last_ticks.pop(symbol, None)
        self._aggregators.pop((symbol, sub.timeframe), None)

        self._event_bus.publish(SymbolDisconnectedEvent(symbol=symbol))
        logger.info("Unsubscribed from %s", symbol)

    @property
    def symbols(self) -> list[str]:
        """Return the list of currently subscribed symbols."""
        return list(self._subscriptions)

    def get_last_tick(self, symbol: str) -> Tick | None:
        """Return the cached latest tick for *symbol*, or ``None``."""
        return self._last_ticks.get(symbol)

    # ------------------------------------------------------------------
    # Service lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        logger.info(
            "Market data service started (poll_interval=%.2fs)",
            self._poll_interval,
        )
        self._scheduler.add_task(
            Task(
                name=self._task_name,
                interval=self._poll_interval,
                action=self._poll_ticks,
            )
        )

    def stop(self) -> None:
        self._scheduler.remove_task(self._task_name)
        self._subscriptions.clear()
        self._last_ticks.clear()
        self._aggregators.clear()
        logger.info("Market data service stopped.")

    # ------------------------------------------------------------------
    # Polling
    # ------------------------------------------------------------------

    def _poll_ticks(self) -> None:
        for symbol, sub in list(self._subscriptions.items()):
            try:
                tick = self._provider.get_tick(symbol)
            except Exception:
                logger.exception("Failed to get tick for %s", symbol)
                continue

            last = self._last_ticks.get(symbol)

            if last is not None:
                if tick.time <= last.time:
                    continue
                # Gap detection logic: if gap > 5 minutes, we missed candles
                if (tick.time - last.time) > timedelta(minutes=5):
                    logger.warning("Data gap detected for %s. Triggering backfill...", symbol)
                    threading.Thread(target=self._preload_history, args=(symbol, sub.timeframe), daemon=True).start()

            self._last_ticks[symbol] = tick
            self._event_bus.publish(TickEvent(tick=tick))
            
            # Feed the tick into the correct BarAggregator
            aggregator = self._aggregators.get((symbol, sub.timeframe))
            if aggregator:
                event = aggregator.update(tick)
                if event:
                    self._event_bus.publish(event)
