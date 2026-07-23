"""
Market data service.

Manages symbol subscriptions, polls MT5 for live ticks, publishes
domain events, and coordinates bar aggregation.
"""

from __future__ import annotations

from tradiba.core.service import Service
from tradiba.events import EventBus
from tradiba.logging import get_logger
from tradiba.mt5.models import Tick
from tradiba.mt5.timeframes import Timeframe
from tradiba.scheduler import Scheduler, Task

from .aggregator import BarAggregator
from .events import (
    SymbolConnectedEvent,
    SymbolDisconnectedEvent,
    TickReceivedEvent,
)
from tradiba.ports.market_data import MarketDataProvider
from .subscriptions import Subscription

logger = get_logger(__name__)

DEFAULT_POLL_INTERVAL: float = 0.2  # seconds


class MarketDataService(Service):
    """
    Polls MT5 for live ticks and publishes market data events.

    Use :meth:`subscribe` / :meth:`unsubscribe` to control which
    symbols are actively polled.  Each new tick is deduplicated
    before being published as a :class:`TickReceivedEvent`.
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
        self._aggregator = BarAggregator(event_bus)
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
        self._aggregator.add_subscription(symbol, timeframe)

        self._event_bus.publish(SymbolConnectedEvent(symbol=symbol))
        logger.info("Subscribed to %s (%s)", symbol, timeframe.name)

    def unsubscribe(self, symbol: str) -> None:
        """Stop monitoring *symbol*."""
        if symbol not in self._subscriptions:
            logger.warning("Not subscribed to %s", symbol)
            return

        del self._subscriptions[symbol]
        self._last_ticks.pop(symbol, None)
        self._aggregator.remove_subscription(symbol)

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
        self._aggregator.clear()
        logger.info("Market data service stopped.")

    # ------------------------------------------------------------------
    # Polling
    # ------------------------------------------------------------------

    def _poll_ticks(self) -> None:
        for symbol in list(self._subscriptions):
            try:
                tick = self._provider.get_tick(symbol)
            except Exception:
                logger.exception("Failed to get tick for %s", symbol)
                continue

            last = self._last_ticks.get(symbol)

            if last is not None and tick.timestamp <= last.timestamp:
                continue

            self._last_ticks[symbol] = tick
            self._event_bus.publish(TickReceivedEvent(tick=tick))
