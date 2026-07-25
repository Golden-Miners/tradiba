from typing import List
from tradiba.events import DomainEvent
from tradiba.mt5.models import Candle
from tradiba.market_structure.state import MarketStructureState
from tradiba.market_structure.models import OrderBlock, Trend, LiquidityStatus
from tradiba.market_structure.events import (
    OrderBlockCreatedEvent,
    OrderBlockMitigatedEvent,
    OrderBlockInvalidatedEvent,
)
from .base import Detector


class OrderBlockDetector(Detector):
    """
    Detects Order Blocks from BOS events and manages their lifecycle.

    Zone lifecycle:
        OPEN → PARTIAL_FILL (price enters the zone)
        OPEN/PARTIAL_FILL → FILLED (price fills the entire zone)
        OPEN → ARCHIVED (price *closes* through the entire OB against its direction)
    """

    def update(self, candle: Candle, state: MarketStructureState, current_events: List[DomainEvent]) -> List[DomainEvent]:
        events: List[DomainEvent] = []

        # 1. Lifecycle management of existing order blocks
        removed_obs: List[OrderBlock] = []
        for ob in state.active_order_blocks:
            if ob.direction == Trend.BULLISH:
                # Bullish OB: we expect price to retrace DOWN into it then bounce
                # Mitigation: price trades fully through the zone (low <= zone_low)
                # Invalidation: price *closes* below zone_low (bearish invalidation)
                if candle.low <= ob.zone_low:
                    ob.status = LiquidityStatus.FILLED
                    removed_obs.append(ob)
                    events.append(OrderBlockMitigatedEvent(ob=ob))
                elif candle.low <= ob.zone_high:
                    ob.status = LiquidityStatus.PARTIAL_FILL
                # Invalidation: price closes decisively below the OB
                if ob not in removed_obs and candle.close < ob.zone_low:
                    ob.status = LiquidityStatus.ARCHIVED
                    removed_obs.append(ob)
                    events.append(OrderBlockInvalidatedEvent(ob=ob))

            elif ob.direction == Trend.BEARISH:
                # Bearish OB: we expect price to retrace UP into it then drop
                # Mitigation: price trades fully through the zone (high >= zone_high)
                # Invalidation: price *closes* above zone_high (bullish invalidation)
                if candle.high >= ob.zone_high:
                    ob.status = LiquidityStatus.FILLED
                    removed_obs.append(ob)
                    events.append(OrderBlockMitigatedEvent(ob=ob))
                elif candle.high >= ob.zone_low:
                    ob.status = LiquidityStatus.PARTIAL_FILL
                # Invalidation: price closes decisively above the OB
                if ob not in removed_obs and candle.close > ob.zone_high:
                    ob.status = LiquidityStatus.ARCHIVED
                    removed_obs.append(ob)
                    events.append(OrderBlockInvalidatedEvent(ob=ob))

        for ob in removed_obs:
            state.active_order_blocks.remove(ob)

        # 2. Check if a BOS occurred in this cycle to create a new Order Block
        for ev in current_events:
            if isinstance(ev, BOSEvent):
                new_ob = self._detect_order_block(state.candles, ev, candle.timestamp, state.candle_count)
                if new_ob:
                    state.active_order_blocks.append(new_ob)
                    events.append(OrderBlockCreatedEvent(ob=new_ob))

        return events

    def _detect_order_block(
        self, candles, bos_event, current_time, candle_count: int,
    ) -> OrderBlock | None:
        if len(candles) < 2:
            return None

        # Look backwards from the BOS candle to find the last opposing candle
        bos_idx = len(candles) - 1

        opposing_candle = None
        if bos_event.direction == Trend.BULLISH:
            # We want the last down-candle (close < open)
            for i in range(bos_idx - 1, -1, -1):
                c = candles[i]
                if c.close < c.open:
                    opposing_candle = c
                    break
        elif bos_event.direction == Trend.BEARISH:
            # We want the last up-candle (close > open)
            for i in range(bos_idx - 1, -1, -1):
                c = candles[i]
                if c.close > c.open:
                    opposing_candle = c
                    break

        if opposing_candle:
            return OrderBlock(
                zone_high=opposing_candle.high,
                zone_low=opposing_candle.low,
                direction=bos_event.direction,
                created_at=current_time,
                status=LiquidityStatus.OPEN,
                originating_bos=bos_event.bos,
                created_candle_count=candle_count,
            )

        return None
