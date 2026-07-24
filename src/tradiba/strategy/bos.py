from __future__ import annotations

from typing import Any

from tradiba.logging import get_logger
from tradiba.strategy.base import Strategy
from tradiba.strategy.models import Direction, Signal
from tradiba.market_structure.events import BreakOfStructureEvent
from tradiba.events import EventBus
from tradiba.strategy.registry import register_strategy

logger = get_logger(__name__)

@register_strategy("bos_strategy")
class BOSStrategy(Strategy):
    """
    A simple strategy that trades Break of Structure (BOS) events.
    - Bullish BOS -> BUY
    - Bearish BOS -> SELL
    """

    def __init__(self, name: str, event_bus: EventBus, config: dict[str, Any]) -> None:
        super().__init__(name, event_bus, config)
        self.symbol = config.get("symbol", "EURUSD")
        self.timeframe = config.get("timeframe", "H1")
        logger.info("BOSStrategy '%s' initialized for %s %s", name, self.symbol, self.timeframe)

    def start(self) -> None:
        self._event_bus.subscribe(BreakOfStructureEvent, self._on_bos)

    def stop(self) -> None:
        self._event_bus.unsubscribe(BreakOfStructureEvent, self._on_bos)

    def _on_bos(self, event: BreakOfStructureEvent) -> None:
        bos = event.bos
        if bos.candle.symbol != self.symbol or bos.candle.timeframe != self.timeframe:
            return

        direction = Direction.LONG if bos.direction.name == "BULLISH" else Direction.SHORT
        
        entry_price = bos.broken_level
        
        if direction == Direction.LONG:
            sl = entry_price - 0.0020
            tp = entry_price + 0.0020
        else:
            sl = entry_price + 0.0020
            tp = entry_price - 0.0020

        signal = Signal(
            strategy_id=self.name,
            symbol=self.symbol,
            direction=direction,
            entry=entry_price,
            stop_loss=sl,
            take_profit=tp,
            confidence=1.0,
        )
        self.publish_signal(signal)
