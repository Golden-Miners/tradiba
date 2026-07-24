from uuid import uuid4

from tradiba.market.models import Candle

from .events import (
    BullishBOSEvent,
    BearishBOSEvent,
    OrderBlockCreatedEvent,
    OrderBlockTouchedEvent,
    OrderBlockMitigatedEvent,
)
from .models import (
    OrderBlock,
    OrderBlockDirection,
    OrderBlockStatus,
)
from .state import MarketStructureState


class OrderBlockDetector:

    def __init__(self):
        self._recent_bullish: Candle | None = None
        self._recent_bearish: Candle | None = None

    def on_bullish_bos(self, event: BullishBOSEvent, state: MarketStructureState):
        events = []
        if self._recent_bearish:
            ob = OrderBlock(
                id=str(uuid4()),
                symbol=event.candle.symbol,
                timeframe=event.candle.timeframe,
                direction=OrderBlockDirection.BULLISH,
                high=self._recent_bearish.high,
                low=self._recent_bearish.low,
                origin_bos_price=event.broken_price,
                created_at=self._recent_bearish.open_time,
                status=OrderBlockStatus.ACTIVE
            )
            state.active_order_blocks.append(ob)
            events.append(OrderBlockCreatedEvent(block=ob))
        return events

    def on_bearish_bos(self, event: BearishBOSEvent, state: MarketStructureState):
        events = []
        if self._recent_bullish:
            ob = OrderBlock(
                id=str(uuid4()),
                symbol=event.candle.symbol,
                timeframe=event.candle.timeframe,
                direction=OrderBlockDirection.BEARISH,
                high=self._recent_bullish.high,
                low=self._recent_bullish.low,
                origin_bos_price=event.broken_price,
                created_at=self._recent_bullish.open_time,
                status=OrderBlockStatus.ACTIVE
            )
            state.active_order_blocks.append(ob)
            events.append(OrderBlockCreatedEvent(block=ob))
        return events

    def update_candle(self, candle: Candle, state: MarketStructureState):
        events = []

        # Check touches and mitigation first
        for ob in state.active_order_blocks:
            if ob.status not in (OrderBlockStatus.ACTIVE, OrderBlockStatus.TOUCHED):
                continue

            # Check touch
            if ob.direction == OrderBlockDirection.BULLISH and candle.low <= ob.high and ob.status == OrderBlockStatus.ACTIVE:
                ob.status = OrderBlockStatus.TOUCHED
                events.append(OrderBlockTouchedEvent(block=ob))
            elif ob.direction == OrderBlockDirection.BEARISH and candle.high >= ob.low and ob.status == OrderBlockStatus.ACTIVE:
                ob.status = OrderBlockStatus.TOUCHED
                events.append(OrderBlockTouchedEvent(block=ob))

            # Check mitigation
            if ob.direction == OrderBlockDirection.BULLISH and candle.close < ob.low:
                ob.status = OrderBlockStatus.MITIGATED
                events.append(OrderBlockMitigatedEvent(block=ob))
            elif ob.direction == OrderBlockDirection.BEARISH and candle.close > ob.high:
                ob.status = OrderBlockStatus.MITIGATED
                events.append(OrderBlockMitigatedEvent(block=ob))

        # Update rolling state
        if candle.close > candle.open:
            self._recent_bullish = candle
        elif candle.close < candle.open:
            self._recent_bearish = candle

        return events
