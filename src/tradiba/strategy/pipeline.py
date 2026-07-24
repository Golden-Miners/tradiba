from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from tradiba.events import EventBus
from tradiba.strategy.models import Signal, Direction
from tradiba.strategy.bias import MarketBias
from tradiba.market.session import SessionName
from tradiba.ports.clock import get_clock


@dataclass(slots=True)
class PipelineContext:
    """
    All inputs needed by the strategy pipeline to evaluate and build a signal.
    """
    symbol: str
    timeframe: str
    confluence_score: int = 0
    confluence_direction: Direction = Direction.LONG
    bias: MarketBias = MarketBias.NEUTRAL
    active_sessions: set[SessionName] = None
    atr: float = 0.0
    spread: float = 0.0
    account_risk_pct: float = 0.01  # 1% of account per trade
    account_balance: float = 10_000.0
    timestamp: Optional[datetime] = None

    def __post_init__(self):
        if self.active_sessions is None:
            self.active_sessions = set()
        if self.timestamp is None:
            self.timestamp = get_clock().now()


class SignalBuilder:
    """
    Centralized factory for TradeSignals.

    Applies ATR-based SL/TP, position sizing from account risk percentage,
    and spread validation.
    """

    def __init__(
        self,
        atr_multiplier_sl: float = 1.5,
        atr_multiplier_tp: float = 3.0,
    ) -> None:
        self.atr_multiplier_sl = atr_multiplier_sl
        self.atr_multiplier_tp = atr_multiplier_tp

    def build(
        self,
        ctx: PipelineContext,
        direction: Direction,
        entry_price: float,
        strategy_id: str = "pipeline",
    ) -> Signal:
        sl_distance = ctx.atr * self.atr_multiplier_sl

        if direction == Direction.LONG:
            sl = entry_price - sl_distance
            tp = entry_price + (ctx.atr * self.atr_multiplier_tp)
        else:
            sl = entry_price + sl_distance
            tp = entry_price - (ctx.atr * self.atr_multiplier_tp)

        # Position sizing: risk = account_balance * risk_pct
        # volume = risk / sl_distance (in price units)
        if sl_distance > 0:
            risk_amount = ctx.account_balance * ctx.account_risk_pct
            volume = round(risk_amount / (sl_distance * 100_000), 2)  # forex: 100k units per lot
            volume = max(0.01, volume)  # minimum micro-lot
        else:
            volume = 0.01

        return Signal(
            symbol=ctx.symbol,
            direction=direction,
            entry=entry_price,
            stop_loss=sl,
            take_profit=tp,
            confidence=ctx.confluence_score,
            strategy_id=strategy_id,
            volume=volume,
        )


class StrategyFilter(ABC):
    """
    A step in the declarative strategy pipeline.
    Returns True if the signal is allowed to proceed, False otherwise.
    """

    @abstractmethod
    def evaluate(self, ctx: PipelineContext) -> bool:
        pass


class ConfluenceFilter(StrategyFilter):
    def __init__(self, min_score: int):
        self.min_score = min_score

    def evaluate(self, ctx: PipelineContext) -> bool:
        return ctx.confluence_score >= self.min_score


class BiasFilter(StrategyFilter):
    def __init__(self, allowed_biases: List[MarketBias]):
        self.allowed_biases = allowed_biases

    def evaluate(self, ctx: PipelineContext) -> bool:
        return ctx.bias in self.allowed_biases


class SessionFilter(StrategyFilter):
    def __init__(self, allowed_sessions: List[SessionName]):
        self.allowed_sessions = allowed_sessions

    def evaluate(self, ctx: PipelineContext) -> bool:
        return any(s in self.allowed_sessions for s in ctx.active_sessions)


class SpreadFilter(StrategyFilter):
    """Rejects signals where spread exceeds a percentage of ATR."""

    def __init__(self, max_spread_pct: float = 0.30):
        self.max_spread_pct = max_spread_pct

    def evaluate(self, ctx: PipelineContext) -> bool:
        if ctx.atr <= 0:
            return True  # can't validate without ATR
        return ctx.spread <= (ctx.atr * self.max_spread_pct)


class StrategyPipeline(ABC):
    """
    Declarative Strategy Pipeline.

    Evaluates a context through a series of filters. If all pass, emits a signal.

    Pipeline stages:
        Market Structure → Confluence → Bias Filter → Session Filter
        → Spread/Risk Filter → Trade Signal
    """

    def __init__(
        self,
        event_bus: EventBus,
        filters: List[StrategyFilter],
        builder: SignalBuilder,
    ) -> None:
        self._event_bus = event_bus
        self._filters = filters
        self._builder = builder

    def execute_pipeline(
        self,
        ctx: PipelineContext,
        entry_price: float,
        strategy_id: str,
    ) -> Optional[Signal]:
        for f in self._filters:
            if not f.evaluate(ctx):
                return None  # Pipeline blocked

        # All filters passed — determine direction from confluence
        if ctx.confluence and ctx.confluence.direction.name == "BULLISH":
            direction = Direction.LONG
        else:
            direction = Direction.SHORT

        signal = self._builder.build(ctx, direction, entry_price, strategy_id)
        return signal
