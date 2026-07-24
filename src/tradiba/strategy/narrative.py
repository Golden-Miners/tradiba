"""
Market Narrative models and service.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List, Set, Optional

from tradiba.core.service import Service
from tradiba.events import EventBus, Event
from tradiba.market.events import CandleClosedEvent
from tradiba.market_structure.models import (
    Trend, LiquidityPool, OrderBlock, FairValueGap
)
from tradiba.market_structure.premium_discount import PDZone, compute_premium_discount
from tradiba.strategy.bias import MarketBias


@dataclass(frozen=True, slots=True)
class MarketNarrative:
    """
    A single, unified snapshot of the market state at a given candle close.
    Strategies consume this instead of querying multiple services directly.
    """
    symbol: str
    timeframe: str
    timestamp: datetime
    
    # Structure
    trend: Trend
    liquidity_pools: List[LiquidityPool]
    active_obs: List[OrderBlock]
    active_fvgs: List[FairValueGap]
    
    # Context
    premium_discount: Optional[PDZone]
    bias: MarketBias
    active_sessions: Set[str]
    confluence_score: int


@dataclass(frozen=True, slots=True)
class NarrativeGeneratedEvent(Event):
    """Published when a new MarketNarrative is generated for a candle."""
    narrative: MarketNarrative


class NarrativeEngine(Service):
    """
    Listens to candle closes, waits for the structural updates to complete 
    (or assumes they are completed sequentially in the same thread), 
    and builds the MarketNarrative.
    """

    def __init__(
        self, 
        event_bus: EventBus,
        market_structure_service,
        market_bias_service,
        session_engine,
        confluence_engine,
    ) -> None:
        self._event_bus = event_bus
        self.ms_service = market_structure_service
        self.bias_service = market_bias_service
        self.session_engine = session_engine
        self.confluence_engine = confluence_engine

    def start(self) -> None:
        # Subscribe to MarketStructureUpdatedEvent if it exists, or CandleClosedEvent
        # If we use CandleClosedEvent, we must ensure ordering (which EventBus handles synchronously)
        # Actually, MarketStructureService emits MarketStructureUpdatedEvent in epic B? Let me check.
        # Epic B actually did not emit a specific "MarketStructureUpdatedEvent", it just emitted the BOS/CHOCH events.
        # But we can listen to CandleClosedEvent with a lower priority if event_bus supported priorities.
        # However, EventBus in tradiba runs handlers in order of subscription. Since NarrativeEngine is registered
        # after MarketStructureService in bootstrap.py, it will receive CandleClosedEvent AFTER MarketStructureService.
        self._event_bus.subscribe(CandleClosedEvent, self.on_candle_closed)

    def stop(self) -> None:
        self._event_bus.unsubscribe(CandleClosedEvent, self.on_candle_closed)

    def on_candle_closed(self, event: CandleClosedEvent) -> None:
        symbol = event.candle.symbol
        timeframe = event.candle.timeframe
        
        # 1. Gather Market Structure
        # Access the timeframe state from MarketStructureService engine
        ms_state = self.ms_service._engine.state.get(symbol)
        if not ms_state:
            return
            
        tf_state = ms_state.get_timeframe_state(timeframe)
        
        # 2. Compute Premium/Discount
        pd = compute_premium_discount(
            event.candle.close, 
            tf_state.last_swing_high, 
            tf_state.last_swing_low
        )
        
        # 3. Gather Bias
        bias = self.bias_service.get_bias(symbol)
        
        # 4. Gather Sessions
        active_sessions = self.session_engine.get_active_sessions()
        
        # 5. Gather Confluence
        confluence_score = self.confluence_engine.get_score(symbol, timeframe)
        
        # 6. Build Narrative
        narrative = MarketNarrative(
            symbol=symbol,
            timeframe=timeframe,
            timestamp=event.candle.timestamp,
            trend=tf_state.trend,
            liquidity_pools=list(tf_state.liquidity_pools),
            active_obs=list(tf_state.active_order_blocks),
            active_fvgs=list(tf_state.active_fvgs),
            premium_discount=pd,
            bias=bias,
            active_sessions=active_sessions,
            confluence_score=confluence_score,
        )
        
        self._event_bus.publish(NarrativeGeneratedEvent(narrative=narrative))
