from tradiba.events import EventBus
from tradiba.mt5.service import MT5Service
from tradiba.execution.adapters.mt5_execution import MT5ExecutionAdapter
from tradiba.execution.service import ExecutionService
from tradiba.strategy import Direction, Signal
from tradiba.execution.events import OrderSubmittedEvent, OrderFilledEvent, OrderRejectedEvent

def test_execution():
    event_bus = EventBus()
    
    events_recorded = []
    
    def on_event(event):
        print(f"Received Event: {event}")
        events_recorded.append(event)
        
    event_bus.subscribe(OrderSubmittedEvent, on_event)
    event_bus.subscribe(OrderFilledEvent, on_event)
    event_bus.subscribe(OrderRejectedEvent, on_event)
    
    # Init MT5
    mt5 = MT5Service()
    mt5.start()
    
    if not mt5.connected:
        print("Failed to connect to MT5.")
        return
        
    execution_adapter = MT5ExecutionAdapter()
    execution_service = ExecutionService(event_bus, execution_adapter)
    execution_service.start()
    
    # Get current price
    tick = mt5.get_tick("EURUSD")
    market_price = tick.ask
    
    signal = Signal(
        symbol="EURUSD",
        direction=Direction.LONG, # renamed from BUY to LONG to match strategy domain
        entry=market_price,
        stop_loss=market_price - 0.0050,
        take_profit=market_price + 0.0050,
        confidence=1.0,
        strategy_id="test_manual",
    )
    
    print(f"Executing manual signal: {signal}")
    execution_service.execute(signal)
    
    mt5.stop()
    print("Test finished.")

if __name__ == "__main__":
    test_execution()
