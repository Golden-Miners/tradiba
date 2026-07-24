from __future__ import annotations

from typing import Any

from tradiba.logging import get_logger
from tradiba.strategy.base import Strategy
from tradiba.strategy.models import Direction, Signal
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
        self.last_trend = None
        logger.info("BOSStrategy '%s' initialized for %s %s", name, self.symbol, self.timeframe)

    def evaluate(self, narrative) -> list[Signal]:
        signals = []
        
        # Detect trend change (which implies a BOS or CHOCH occurred)
        if self.last_trend is not None and narrative.trend != self.last_trend:
            direction = Direction.LONG if narrative.trend.name == "BULLISH" else Direction.SHORT
            
            # Simple entry based on current price (assuming narrative has timestamp, but we don't have current price in narrative)
            # Wait, the MarketNarrative doesn't have current price? We can use an active OB's zone_low/high.
            # Or we can just use the latest OB.
            if narrative.active_obs:
                latest_ob = narrative.active_obs[-1]
                entry_price = latest_ob.zone_low if direction == Direction.LONG else latest_ob.zone_high
                
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
                signals.append(signal)

        self.last_trend = narrative.trend
        return signals
