from tradiba.resilience.reconciliation import ReconciliationEngine
from tradiba.events import EventBus

def test_reconciliation():
    bus = EventBus()
    engine = ReconciliationEngine(event_bus=bus)
    
    internal_pos = {"AAPL": 100.0, "TSLA": 50.0}
    broker_pos = {"AAPL": 100.0, "TSLA": 40.0, "MSFT": 10.0}
    
    discrepancies = engine.reconcile_positions(internal_pos, broker_pos)
    
    assert "AAPL" not in discrepancies
    assert discrepancies["TSLA"] == 10.0  # Internal has 10 more than broker
    assert discrepancies["MSFT"] == -10.0 # Internal is missing 10
