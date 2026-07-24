from enum import Enum, auto
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from tradiba.events import EventBus, Event
from tradiba.market_structure.models import Trend
from tradiba.market_structure.events import TrendChangedEvent


class MarketBias(Enum):
    STRONG_BULLISH = auto()
    BULLISH = auto()
    NEUTRAL = auto()
    BEARISH = auto()
    STRONG_BEARISH = auto()


@dataclass(frozen=True, slots=True)
class BiasComputedEvent(Event):
    symbol: str
    bias: MarketBias


# Default timeframe hierarchy with weights (higher timeframe = more weight)
_DEFAULT_HIERARCHY: List[Tuple[str, int]] = [
    ("H4", 3),
    ("H1", 2),
    ("M15", 1),
]


class MarketBiasService:
    """
    Computes overall market bias from multi-timeframe trend alignment.

    Uses weighted scoring: higher timeframes carry more weight.
    The hierarchy and weights are configurable.

    Bias thresholds (percentage of max weighted score):
        >= 80% → STRONG_BULLISH / STRONG_BEARISH
        >= 40% → BULLISH / BEARISH
        else   → NEUTRAL
    """

    def __init__(
        self,
        event_bus: EventBus,
        hierarchy: Optional[List[Tuple[str, int]]] = None,
    ) -> None:
        self._event_bus = event_bus
        self._hierarchy = hierarchy or _DEFAULT_HIERARCHY
        self._max_score = sum(w for _, w in self._hierarchy)
        # symbol -> timeframe -> Trend
        self._trends: Dict[str, Dict[str, Trend]] = {}
        # symbol -> current bias (for query access)
        self._current_bias: Dict[str, MarketBias] = {}

    def start(self) -> None:
        self._event_bus.subscribe(TrendChangedEvent, self._on_trend_changed)

    def stop(self) -> None:
        self._event_bus.unsubscribe(TrendChangedEvent, self._on_trend_changed)

    def get_bias(self, symbol: str) -> MarketBias:
        """Query the current overall market bias for a symbol."""
        return self._current_bias.get(symbol, MarketBias.NEUTRAL)

    def _on_trend_changed(self, event: TrendChangedEvent) -> None:
        if event.symbol not in self._trends:
            self._trends[event.symbol] = {}

        self._trends[event.symbol][event.timeframe] = event.new_trend
        self._recompute_bias(event.symbol)

    def _recompute_bias(self, symbol: str) -> None:
        symbol_trends = self._trends.get(symbol, {})

        # Compute weighted score: +weight for bullish, -weight for bearish, 0 for neutral
        weighted_score = 0
        for tf, weight in self._hierarchy:
            trend = symbol_trends.get(tf, Trend.NEUTRAL)
            if trend == Trend.BULLISH:
                weighted_score += weight
            elif trend == Trend.BEARISH:
                weighted_score -= weight

        # Determine bias from weighted score as percentage of max
        if self._max_score == 0:
            bias = MarketBias.NEUTRAL
        else:
            pct = abs(weighted_score) / self._max_score
            if weighted_score > 0:
                bias = MarketBias.STRONG_BULLISH if pct >= 0.80 else MarketBias.BULLISH if pct >= 0.40 else MarketBias.NEUTRAL
            elif weighted_score < 0:
                bias = MarketBias.STRONG_BEARISH if pct >= 0.80 else MarketBias.BEARISH if pct >= 0.40 else MarketBias.NEUTRAL
            else:
                bias = MarketBias.NEUTRAL

        self._current_bias[symbol] = bias
        self._event_bus.publish(BiasComputedEvent(symbol=symbol, bias=bias))
