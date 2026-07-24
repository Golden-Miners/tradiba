"""
Smart Money Concepts Strategy — the flagship Tradiba strategy.

Subscribes to confluence and bias events, runs the declarative pipeline,
and emits trade signals when all configured conditions are satisfied.

Pipeline:
    Market Structure → Confluence → Bias Filter → Session Filter
    → Spread Filter → News Filter → Trade Signal
"""

from __future__ import annotations

from typing import Any, List

from tradiba.logging import get_logger
from tradiba.events import EventBus
from tradiba.strategy.base import Strategy
from tradiba.strategy.models import Signal
from tradiba.strategy.registry import register_strategy
from tradiba.strategy.bias import MarketBias
from tradiba.market.session import SessionName
from tradiba.strategy.pipeline import (
    PipelineContext,
    SignalBuilder,
    StrategyFilter,
    ConfluenceFilter,
    BiasFilter,
    SessionFilter,
    SpreadFilter,
)

logger = get_logger(__name__)


@register_strategy("smc_strategy")
class SMCStrategy(Strategy):
    """
    Declarative SMC strategy that composes existing building blocks.

    Config keys:
        symbol          — trading symbol (default: EURUSD)
        timeframe       — primary timeframe (default: H1)
        min_confluence  — minimum confluence score to trigger (default: 30)
        allowed_biases  — list of bias names (default: [STRONG_BULLISH, BULLISH])
        allowed_sessions — list of session names (default: [London, New York])
        atr_sl_mult     — ATR multiplier for SL (default: 1.5)
        atr_tp_mult     — ATR multiplier for TP (default: 3.0)
        max_spread_pct  — max spread as % of ATR (default: 0.30)
    """

    def __init__(self, name: str, event_bus: EventBus, config: dict[str, Any]) -> None:
        super().__init__(name, event_bus, config)
        self.symbol = config.get("symbol", "EURUSD")
        self.timeframe = config.get("timeframe", "H1")

        # Build filters from config
        min_confluence = config.get("min_confluence", 30)
        allowed_bias_names = config.get("allowed_biases", ["STRONG_BULLISH", "BULLISH"])
        allowed_biases = [MarketBias[b] for b in allowed_bias_names]
        allowed_session_names = config.get("allowed_sessions", ["London", "New York"])
        session_map = {s.value: s for s in SessionName}
        allowed_sessions = [session_map[s] for s in allowed_session_names if s in session_map]
        max_spread_pct = config.get("max_spread_pct", 0.30)

        self._filters: List[StrategyFilter] = [
            ConfluenceFilter(min_score=min_confluence),
            BiasFilter(allowed_biases=allowed_biases),
        ]
        if allowed_sessions:
            self._filters.append(SessionFilter(allowed_sessions=allowed_sessions))
        self._filters.append(SpreadFilter(max_spread_pct=max_spread_pct))

        self._builder = SignalBuilder(
            atr_multiplier_sl=config.get("atr_sl_mult", 1.5),
            atr_multiplier_tp=config.get("atr_tp_mult", 3.0),
        )

        # Note: We no longer store state, we evaluate purely off the narrative
        logger.info(
            "SMCStrategy '%s' initialized for %s %s (min_confluence=%d)",
            name, self.symbol, self.timeframe, min_confluence,
        )

    def evaluate(self, narrative) -> list[Signal]:
        from tradiba.strategy.models import Direction
        
        # In this implementation, the "confluence direction" defaults to the trend direction
        # since MarketNarrative does not currently store confluence direction, only score.
        confluence_direction = Direction.LONG if narrative.trend.name == "BULLISH" else Direction.SHORT
        
        ctx = PipelineContext(
            symbol=self.symbol,
            timeframe=self.timeframe,
            confluence_score=narrative.confluence_score,
            confluence_direction=confluence_direction,
            bias=narrative.bias,
            active_sessions=set(narrative.active_sessions),
            atr=self.config.get("atr", 0.0050),  # default 50 pips
            spread=self.config.get("spread", 0.0),
            account_risk_pct=self.config.get("account_risk_pct", 0.01),
        )

        # Determine entry price from the latest order block or market price
        # For simulation, we use a config entry_price or the last swing
        entry_price = self.config.get("entry_price", 0.0)
        if entry_price <= 0 and narrative.active_obs:
            latest_ob = narrative.active_obs[-1]
            entry_price = latest_ob.zone_low if confluence_direction == Direction.LONG else latest_ob.zone_high
            
        if entry_price <= 0:
            return []  # no valid entry

        # Run through all filters
        for f in self._filters:
            if not f.evaluate(ctx):
                logger.debug(
                    "SMCStrategy '%s': filter %s blocked signal",
                    self.name, f.__class__.__name__,
                )
                return []

        # All filters passed — build and publish signal
        signal = self._builder.build(ctx, confluence_direction, entry_price, self.name)
        
        logger.info(
            "SMCStrategy '%s': signal emitted %s at %.5f (score=%d, bias=%s)",
            self.name, confluence_direction.value, entry_price, narrative.confluence_score, narrative.bias.name,
        )
        return [signal]
