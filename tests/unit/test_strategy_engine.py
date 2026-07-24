import pytest
from datetime import datetime, timezone
from tradiba.market_structure.models import Trend
from tradiba.market_structure.narrative import MarketNarrative, MarketBias
from tradiba.strategy.models import TradingSignal, SignalSide, SignalStrength
from tradiba.strategy.interface import Strategy
from tradiba.strategy.registry import StrategyRegistry
from tradiba.strategy.validator import SignalValidator
from tradiba.strategy.manager import StrategyManager
from tradiba.strategy.resolver import ConflictResolver
from tradiba.strategy.engine import StrategyEngine
from tradiba.strategy.exceptions import StrategyRegistrationError

class DummyStrategy(Strategy):
    name = "dummy_1"
    priority = 10
    enabled = True

    def __init__(self, signals):
        self._signals = signals

    def evaluate(self, narrative):
        return self._signals

def create_narrative():
    return MarketNarrative(
        symbol="EURUSD",
        timeframe="H1",
        current_price=1.10,
        timestamp=datetime.now(timezone.utc),
        trend=Trend.BULLISH,
        bias=MarketBias.BULLISH,
        confidence=80
    )

def create_signal(strategy, side, confidence, entry, stop_loss, take_profit):
    return TradingSignal(
        strategy=strategy,
        symbol="EURUSD",
        timeframe="H1",
        side=side,
        strength=SignalStrength.STRONG,
        confidence=confidence,
        entry=entry,
        stop_loss=stop_loss,
        take_profit=take_profit,
        created_at=datetime.now(timezone.utc),
        metadata={}
    )

def test_registry_registration():
    reg = StrategyRegistry()
    s1 = DummyStrategy([])
    reg.register(s1)
    
    assert len(reg.strategies()) == 1
    
    # Duplicate
    with pytest.raises(StrategyRegistrationError):
        reg.register(s1)

def test_strategy_priority_ordering():
    reg = StrategyRegistry()
    s1 = DummyStrategy([])
    s1.name = "s1"
    s1.priority = 50
    
    s2 = DummyStrategy([])
    s2.name = "s2"
    s2.priority = 10
    
    reg.register(s1)
    reg.register(s2)
    
    strats = reg.strategies()
    assert strats[0].name == "s2"
    assert strats[1].name == "s1"

def test_disabled_strategies_skipped():
    reg = StrategyRegistry()
    s1 = DummyStrategy([])
    s1.name = "s1"
    s1.enabled = False
    
    reg.register(s1)
    assert len(reg.strategies()) == 0

def test_invalid_signals_rejected():
    v = SignalValidator()
    # Invalid (confidence < 50)
    sig1 = create_signal("s1", SignalSide.BUY, 40, 1.10, 1.09, 1.11)
    # Invalid (entry 0)
    sig2 = create_signal("s1", SignalSide.BUY, 80, 0, 1.09, 1.11)
    # Valid
    sig3 = create_signal("s1", SignalSide.BUY, 80, 1.10, 1.09, 1.11)
    
    assert not v.validate(sig1)
    assert not v.validate(sig2)
    assert v.validate(sig3)

def test_multiple_strategies_producing_valid_signals():
    reg = StrategyRegistry()
    v = SignalValidator()
    
    sig1 = create_signal("s1", SignalSide.BUY, 80, 1.10, 1.09, 1.11)
    sig2 = create_signal("s2", SignalSide.BUY, 85, 1.10, 1.09, 1.11)
    
    s1 = DummyStrategy([sig1])
    s1.name = "s1"
    
    s2 = DummyStrategy([sig2])
    s2.name = "s2"
    
    reg.register(s1)
    reg.register(s2)
    
    manager = StrategyManager(reg, v)
    narrative = create_narrative()
    signals = manager.evaluate(narrative)
    
    assert len(signals) == 2

def test_conflict_resolution_and_deterministic_ordering():
    sig_buy = create_signal("s_buy", SignalSide.BUY, 80, 1.10, 1.09, 1.11)
    sig_sell = create_signal("s_sell", SignalSide.SELL, 50, 1.10, 1.11, 1.09)
    
    reg = StrategyRegistry()
    v = SignalValidator()
    
    s1 = DummyStrategy([sig_buy])
    s1.name = "s_buy"
    
    s2 = DummyStrategy([sig_sell])
    s2.name = "s_sell"
    
    reg.register(s1)
    reg.register(s2)
    
    manager = StrategyManager(reg, v)
    resolver = ConflictResolver(margin=20)
    engine = StrategyEngine(manager, resolver)
    
    narrative = create_narrative()
    signals = engine.process(narrative)
    
    # buy dominates: 80 vs 50. Margin is 20, 80 > 50 + 20 => True
    assert len(signals) == 1
    assert signals[0].side == SignalSide.BUY

def test_conflict_resolution_no_dominance():
    sig_buy = create_signal("s_buy", SignalSide.BUY, 60, 1.10, 1.09, 1.11)
    sig_sell = create_signal("s_sell", SignalSide.SELL, 70, 1.10, 1.11, 1.09)
    
    resolver = ConflictResolver(margin=20)
    signals = resolver.resolve([sig_buy, sig_sell])
    
    # 70 vs 60, margin is 20. 70 is not > 60 + 20. No dominance.
    assert len(signals) == 0

def test_no_signals_produced():
    reg = StrategyRegistry()
    v = SignalValidator()
    s1 = DummyStrategy([])
    s1.name = "s1"
    reg.register(s1)
    
    engine = StrategyEngine(StrategyManager(reg, v), ConflictResolver())
    narrative = create_narrative()
    signals = engine.process(narrative)
    
    assert len(signals) == 0
