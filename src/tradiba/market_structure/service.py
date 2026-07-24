"""
Market structure analysis service.

Subscribes to :class:`CandleClosedEvent` and pushes candles through the
MarketStructureEngine, publishing SMC domain events.
"""

from __future__ import annotations

from tradiba.core.service import Service
from tradiba.events import EventBus
from tradiba.logging import get_logger
from tradiba.market.events import CandleClosedEvent
from tradiba.market_structure.engine import MarketStructureEngine

logger = get_logger(__name__)


class MarketStructureService(Service):
    """
    Subscribes to incoming candles, feeds them to the MarketStructureEngine,
    and publishes the resulting events to the EventBus.
    """

    def __init__(self, event_bus: EventBus) -> None:
        self._event_bus = event_bus
        self._engine = MarketStructureEngine()

    def start(self) -> None:
        self._event_bus.subscribe(CandleClosedEvent, self._on_candle)
        logger.info("Market structure service started.")

    def stop(self) -> None:
        self._event_bus.unsubscribe(CandleClosedEvent, self._on_candle)
        logger.info("Market structure service stopped.")

    def _on_candle(self, event: CandleClosedEvent) -> None:
        candle = event.candle
        
        # Pass candle to pure domain engine
        new_events = self._engine.on_candle(candle)
            
        # Publish all generated events for the cycle
        for ev in new_events:
            self._event_bus.publish(ev)
            logger.debug("Published market structure event: %s", ev.__class__.__name__)
