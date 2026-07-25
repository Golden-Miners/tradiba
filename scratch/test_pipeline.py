from tradiba.events import EventBus
from tradiba.mt5.service import MT5Service
from tradiba.execution.adapters.mt5_execution import MT5ExecutionAdapter
from tradiba.execution.service import ExecutionService
from tradiba.strategy import Direction, Signal
from tradiba.strategy.events import TradingSignalCreatedEvent
from tradiba.execution.events import OrderSubmittedEvent, OrderFilledEvent, OrderRejectedEvent
from tradiba.risk.service import RiskService
from tradiba.risk.events import TradeApprovedEvent, TradeRejectedEvent
from tradiba.risk.rules.max_position_size import MaximumPositionSizeRule
from tradiba.portfolio.service import PortfolioService
from tradiba.portfolio.events import PortfolioUpdatedEvent

def test_pipeline():
    event_bus = EventBus()
    
    events_recorded = []
    def on_event(event):
        print(f"Received Event: {type(event).__name__}")
        events_recorded.append(event)
        
    event_bus.subscribe(OrderSubmittedEvent, on_event)
    event_bus.subscribe(OrderFilledEvent, on_event)
    event_bus.subscribe(OrderRejectedEvent, on_event)
    event_bus.subscribe(TradeApprovedEvent, on_event)
    event_bus.subscribe(TradeRejectedEvent, on_event)
    event_bus.subscribe(PortfolioUpdatedEvent, on_event)
    
    mt5 = MT5Service()
    mt5.start()
    
    if not mt5.connected:
        print("Failed to connect to MT5.")
        return
        
    execution_adapter = MT5ExecutionAdapter()
    execution_service = ExecutionService(event_bus, execution_adapter)
    execution_service.start()
    
    portfolio_service = PortfolioService(event_bus, execution_adapter)
    portfolio_service.start()
    
    risk_service = RiskService(event_bus)
    # 2.0 max volume
    risk_service.add_rule(MaximumPositionSizeRule(2.0))
    risk_service.start()
    
    tick = mt5.get_tick("EURUSD")
    market_price = tick.ask
    
    print("\n--- Test 1: Invalid Signal (Volume = 10) ---")
    invalid_signal = Signal(
        symbol="EURUSD",
        direction=Direction.LONG,
        entry=market_price,
        stop_loss=market_price - 0.0050,
        take_profit=market_price + 0.0050,
        confidence=1.0,
        strategy_id="test_risk",
        volume=10.0,
    )
    event_bus.publish(TradingSignalCreatedEvent(signal=invalid_signal))
    
    print("\n--- Test 2: Valid Signal (Volume = 0.01) ---")
    valid_signal = Signal(
        symbol="EURUSD",
        direction=Direction.LONG,
        entry=market_price,
        stop_loss=market_price - 0.0050,
        take_profit=market_price + 0.0050,
        confidence=1.0,
        strategy_id="test_risk",
        volume=0.01,
    )
    event_bus.publish(TradingSignalCreatedEvent(signal=valid_signal))
    
    mt5.stop()
    print("Test finished.")

if __name__ == "__main__":
    test_pipeline()
