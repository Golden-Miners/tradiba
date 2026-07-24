from uuid import uuid4

from tradiba.market.models import Candle

from .events import (
    LiquidityCreatedEvent,
    LiquiditySweptEvent,
)
from .models import (
    LiquidityPool,
    LiquidityStatus,
    LiquidityType,
    SwingPoint,
    SwingType,
)
from .state import MarketStructureState


class LiquidityDetector:

    def __init__(self, tolerance: float = 0.00010, min_touches: int = 2):
        self._tolerance = tolerance
        self._min_touches = min_touches

    def update_swing(self, swing: SwingPoint, state: MarketStructureState):
        events = []

        liquidity_type = (
            LiquidityType.BUY_SIDE
            if swing.type is SwingType.HIGH
            else LiquidityType.SELL_SIDE
        )

        for pool in state.active_liquidity:
            if pool.status != LiquidityStatus.ACTIVE:
                continue
                
            if pool.liquidity_type != liquidity_type:
                continue

            if abs(pool.price - swing.price) <= self._tolerance:
                pool.touches += 1
                
                # Emit event when the pool reaches the minimum required touches
                if pool.touches == self._min_touches:
                    events.append(LiquidityCreatedEvent(pool=pool))
                    
                return events

        pool = LiquidityPool(
            id=str(uuid4()),
            symbol=swing.symbol,
            timeframe=swing.timeframe,
            price=swing.price,
            liquidity_type=liquidity_type,
            touches=1,
            tolerance=self._tolerance,
            created_at=swing.candle_time,
        )

        state.active_liquidity.append(pool)

        if self._min_touches == 1:
            events.append(LiquidityCreatedEvent(pool=pool))

        return events

    def check_sweep(self, candle: Candle, state: MarketStructureState):
        events = []

        for pool in state.active_liquidity:
            if pool.status != LiquidityStatus.ACTIVE:
                continue
                
            # Only valid liquidity pools can be swept
            if pool.touches < self._min_touches:
                continue

            if (
                pool.liquidity_type is LiquidityType.BUY_SIDE
                and candle.high > pool.price
            ):
                pool.status = LiquidityStatus.SWEPT
                events.append(LiquiditySweptEvent(pool=pool))

            elif (
                pool.liquidity_type is LiquidityType.SELL_SIDE
                and candle.low < pool.price
            ):
                pool.status = LiquidityStatus.SWEPT
                events.append(LiquiditySweptEvent(pool=pool))

        return events
