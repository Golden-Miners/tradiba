from typing import List
from tradiba.events import DomainEvent
from tradiba.mt5.models import Candle
from tradiba.market_structure.state import MarketStructureState
from tradiba.market_structure.models import LiquidityPool, Trend, SwingPoint, LiquidityStatus
from tradiba.market_structure.events import (
    LiquidityCreatedEvent,
    LiquiditySweptEvent,
)
from .base import Detector


class LiquidityDetector(Detector):
    """
    Detects liquidity pools from clusters of equal highs/lows
    and manages their lifecycle.

    Zone lifecycle:
        OPEN → PARTIAL_FILL (price approaches the pool within tolerance)
        OPEN/PARTIAL_FILL → FILLED (price sweeps through the pool)
    """

    def __init__(self, tolerance_pts: float = 2.0) -> None:
        self.tolerance_pts = tolerance_pts

    def update(self, candle: Candle, state: MarketStructureState, current_events: List[DomainEvent]) -> List[DomainEvent]:
        events: List[DomainEvent] = []

        # 1. Lifecycle management of existing pools
        removed_pools: List[LiquidityPool] = []
        for pool in state.liquidity_pools:
            if pool.direction == Trend.BULLISH:  # Equal Highs (Buy Side Liquidity)
                if candle.high > pool.price:
                    pool.status = LiquidityStatus.FILLED
                    events.append(LiquiditySweptEvent(pool=pool, candle=candle))
                    removed_pools.append(pool)
                elif candle.high >= pool.price - self.tolerance_pts:
                    pool.status = LiquidityStatus.PARTIAL_FILL
            elif pool.direction == Trend.BEARISH:  # Equal Lows (Sell Side Liquidity)
                if candle.low < pool.price:
                    pool.status = LiquidityStatus.FILLED
                    events.append(LiquiditySweptEvent(pool=pool, candle=candle))
                    removed_pools.append(pool)
                elif candle.low <= pool.price + self.tolerance_pts:
                    pool.status = LiquidityStatus.PARTIAL_FILL

        for p in removed_pools:
            state.liquidity_pools.remove(p)

        # 2. Detect new pools from unmitigated swings
        # Buy Side Liquidity (Equal Highs)
        self._detect_clusters(
            state.unmitigated_swing_highs, state.liquidity_pools,
            events, Trend.BULLISH, candle.timestamp,
        )
        # Sell Side Liquidity (Equal Lows)
        self._detect_clusters(
            state.unmitigated_swing_lows, state.liquidity_pools,
            events, Trend.BEARISH, candle.timestamp,
        )

        return events

    def _detect_clusters(
        self,
        unmitigated_swings: List[SwingPoint],
        pools: List[LiquidityPool],
        events: List[DomainEvent],
        direction: Trend,
        current_time,
    ) -> None:
        if len(unmitigated_swings) < 2:
            return

        # Simple clustering: compare newest swing to previous ones
        newest = unmitigated_swings[-1]

        cluster = [newest]
        for swing in unmitigated_swings[:-1]:
            if abs(swing.price - newest.price) <= self.tolerance_pts:
                cluster.append(swing)

        if len(cluster) >= 2:
            avg_price = sum(s.price for s in cluster) / len(cluster)

            pool = LiquidityPool(
                price=avg_price,
                strength=len(cluster),
                direction=direction,
                created_at=current_time,
            )
            pools.append(pool)
            events.append(LiquidityCreatedEvent(pool=pool))

            # Consume the swings so they don't form duplicate pools
            for s in cluster:
                unmitigated_swings.remove(s)
