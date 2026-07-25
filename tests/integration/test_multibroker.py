import pytest
from tradiba.brokers.registry import BrokerRegistry
from tradiba.brokers.discovery import ExecutionCapabilityNegotiator
from tradiba.brokers.routing import OrderRouter
from tradiba.brokers.adapters.mt5 import MT5BrokerAdapter
from tradiba.brokers.exceptions import RoutingError
from tradiba.strategy.models import TradingSignal, SignalSide, SignalStrength
from datetime import datetime

def test_broker_registration():
    registry = BrokerRegistry()
    adapter = MT5BrokerAdapter()
    
    registry.register("MT5", adapter)
    assert registry.get("MT5") == adapter
    assert len(registry.list()) == 1

    registry.unregister("MT5")
    assert registry.get("MT5") is None

def test_order_routing_default():
    registry = BrokerRegistry()
    adapter = MT5BrokerAdapter()
    registry.register("MT5", adapter)
    
    negotiator = ExecutionCapabilityNegotiator()
    router = OrderRouter(registry, negotiator)
    
    signal = TradingSignal(
        strategy="test",
        symbol="EURUSD",
        timeframe="M1",
        side=SignalSide.BUY,
        strength=SignalStrength.NORMAL,
        confidence=80,
        entry=1.1,
        stop_loss=1.0,
        take_profit=1.2,
        created_at=datetime.now(),
        metadata={}
    )
    
    # Should route to MT5 by default (first available)
    # The submit method of the stub returns None
    result = router.route(signal)
    assert result is None

def test_order_routing_preferred():
    registry = BrokerRegistry()
    adapter1 = MT5BrokerAdapter()
    adapter2 = MT5BrokerAdapter()
    
    registry.register("MT5_1", adapter1)
    registry.register("MT5_2", adapter2)
    
    negotiator = ExecutionCapabilityNegotiator()
    router = OrderRouter(registry, negotiator)
    
    signal = TradingSignal(
        strategy="test",
        symbol="EURUSD",
        timeframe="M1",
        side=SignalSide.BUY,
        strength=SignalStrength.NORMAL,
        confidence=80,
        entry=1.1,
        stop_loss=1.0,
        take_profit=1.2,
        created_at=datetime.now(),
        metadata={}
    )
    
    # Route to preferred broker
    result = router.route(signal, preferred_broker="MT5_2")
    assert result is None

def test_routing_error_not_found():
    registry = BrokerRegistry()
    negotiator = ExecutionCapabilityNegotiator()
    router = OrderRouter(registry, negotiator)
    
    signal = TradingSignal(
        strategy="test",
        symbol="EURUSD",
        timeframe="M1",
        side=SignalSide.BUY,
        strength=SignalStrength.NORMAL,
        confidence=80,
        entry=1.1,
        stop_loss=1.0,
        take_profit=1.2,
        created_at=datetime.now(),
        metadata={}
    )
    
    with pytest.raises(RoutingError):
        router.route(signal)
