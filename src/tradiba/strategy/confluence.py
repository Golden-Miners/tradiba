from dataclasses import dataclass
from typing import List, Dict, Optional
from tradiba.events import Event, EventBus
from tradiba.market_structure.models import Trend
from tradiba.market_structure.events import (
    BOSEvent, CHOCHEvent, LiquiditySweptEvent,
    OrderBlockCreatedEvent, FairValueGapCreatedEvent,
)


@dataclass(slots=True)
class ConfluenceWeights:
    """Configurable point values for each signal type."""
    bos: int = 30
    choch: int = 20
    liquidity_sweep: int = 20
    order_block: int = 20
    fvg: int = 10


@dataclass(slots=True)
class Confluence:
    score: int
    direction: Trend
    reasons: List[str]


@dataclass(frozen=True, slots=True)
class ConfluenceComputedEvent(Event):
    symbol: str
    timeframe: str
    confluence: Confluence


class ConfluenceEngine:
    """
    Listens to market structure events and maintains a running confluence score.

    On CHOCH (trend reversal), the score for that symbol/timeframe is reset to zero
    so stale signals from the previous trend don't carry over.
    """

    def __init__(
        self,
        event_bus: EventBus,
        weights: Optional[ConfluenceWeights] = None,
        max_reasons: int = 10,
    ) -> None:
        self._event_bus = event_bus
        self._weights = weights or ConfluenceWeights()
        self._max_reasons = max_reasons
        self._scores: Dict[tuple[str, str], int] = {}
        self._reasons: Dict[tuple[str, str], List[str]] = {}

    def start(self) -> None:
        self._event_bus.subscribe(BOSEvent, self._on_bos)
        self._event_bus.subscribe(CHOCHEvent, self._on_choch)
        self._event_bus.subscribe(LiquiditySweptEvent, self._on_liquidity)
        self._event_bus.subscribe(OrderBlockCreatedEvent, self._on_ob)
        self._event_bus.subscribe(FairValueGapCreatedEvent, self._on_fvg)

    def get_score(self, symbol: str, timeframe: str) -> int:
        """Returns the absolute confluence score for a symbol/timeframe."""
        return abs(self._scores.get((symbol, timeframe), 0))

    def stop(self) -> None:
        self._event_bus.unsubscribe(BOSEvent, self._on_bos)
        self._event_bus.unsubscribe(CHOCHEvent, self._on_choch)
        self._event_bus.unsubscribe(LiquiditySweptEvent, self._on_liquidity)
        self._event_bus.unsubscribe(OrderBlockCreatedEvent, self._on_ob)
        self._event_bus.unsubscribe(FairValueGapCreatedEvent, self._on_fvg)

    def get_confluence(self, symbol: str, timeframe: str) -> Optional[Confluence]:
        """Query the current confluence for a symbol/timeframe pair."""
        key = (symbol, timeframe)
        if key not in self._scores:
            return None
        current_score = self._scores[key]
        if current_score > 0:
            direction = Trend.BULLISH
        elif current_score < 0:
            direction = Trend.BEARISH
        else:
            direction = Trend.NEUTRAL
        return Confluence(
            score=abs(current_score),
            direction=direction,
            reasons=list(self._reasons.get(key, [])),
        )

    def _reset(self, symbol: str, timeframe: str) -> None:
        """Reset confluence score on trend reversal (CHOCH)."""
        key = (symbol, timeframe)
        self._scores[key] = 0
        self._reasons[key] = []

    def _update_score(
        self, symbol: str, timeframe: str, direction: Trend, points: int, reason: str,
    ) -> None:
        key = (symbol, timeframe)
        if key not in self._scores:
            self._scores[key] = 0
            self._reasons[key] = []

        # Direction implies sign (+ for Bullish, - for Bearish)
        modifier = 1 if direction == Trend.BULLISH else -1
        self._scores[key] += points * modifier

        self._reasons[key].append(f"{reason} ({direction.value})")

        # Keep reasons bounded
        if len(self._reasons[key]) > self._max_reasons:
            self._reasons[key].pop(0)

        current_score = self._scores[key]
        if current_score > 0:
            overall_direction = Trend.BULLISH
        elif current_score < 0:
            overall_direction = Trend.BEARISH
        else:
            overall_direction = Trend.NEUTRAL

        confluence = Confluence(
            score=abs(current_score),
            direction=overall_direction,
            reasons=list(self._reasons[key]),
        )

        self._event_bus.publish(ConfluenceComputedEvent(
            symbol=symbol, timeframe=timeframe, confluence=confluence,
        ))

    def _on_bos(self, event: BOSEvent) -> None:
        self._update_score(
            event.symbol, event.candle.timeframe, event.direction,
            self._weights.bos, "BOS",
        )

    def _on_choch(self, event: CHOCHEvent) -> None:
        # A CHOCH reverses the trend — reset confluence, then add the new signal
        symbol = event.choch.candle.symbol
        timeframe = event.choch.candle.timeframe
        self._reset(symbol, timeframe)
        self._update_score(
            symbol, timeframe, event.choch.direction,
            self._weights.choch, "CHOCH",
        )

    def _on_liquidity(self, event: LiquiditySweptEvent) -> None:
        # Sweeping sell-side liquidity (bearish pool) usually precedes a bullish move
        direction = Trend.BULLISH if event.pool.direction == Trend.BEARISH else Trend.BEARISH
        self._update_score(
            event.candle.symbol, event.candle.timeframe, direction,
            self._weights.liquidity_sweep, "Liquidity Sweep",
        )

    def _on_ob(self, event: OrderBlockCreatedEvent) -> None:
        self._update_score(
            event.ob.originating_bos.candle.symbol,
            event.ob.originating_bos.candle.timeframe,
            event.ob.originating_bos.direction,
            self._weights.order_block, "Order Block",
        )

    def _on_fvg(self, event: FairValueGapCreatedEvent) -> None:
        self._update_score(
            event.symbol, event.timeframe, event.fvg.direction,
            self._weights.fvg, "Fair Value Gap",
        )
