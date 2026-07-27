from tradiba.integrations.synchronization.failover import FailoverManager
from tradiba.integrations.brokers.paper.adapter import PaperBrokerAdapter

class FailingAdapter(PaperBrokerAdapter):
    def connect(self) -> bool:
        return False

def test_failover_manager():
    primary = FailingAdapter()
    secondary = PaperBrokerAdapter()
    
    manager = FailoverManager(primary=primary, secondaries=[secondary])
    
    assert manager.get_active_adapter() == primary
    
    # Check health should trigger failover
    manager.check_health()
    
    assert manager.get_active_adapter() == secondary
