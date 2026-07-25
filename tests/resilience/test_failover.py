from tradiba.resilience.failover import FailoverManager
from tradiba.events import EventBus

def test_failover_manager():
    bus = EventBus()
    manager = FailoverManager(event_bus=bus)
    
    assert len(manager._active_secondaries) == 0
    
    manager.promote_secondary("market_data", "secondary_provider")
    assert "market_data" in manager._active_secondaries
    
    manager.rollback("market_data")
    assert "market_data" not in manager._active_secondaries
