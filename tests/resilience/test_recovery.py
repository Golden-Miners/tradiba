import pytest
from tradiba.resilience.recovery import RecoveryManager
from tradiba.resilience.checkpoint import InMemoryCheckpointRepository
from tradiba.events import EventBus
from tradiba.resilience.exceptions import RecoveryError

def test_recovery_manager():
    bus = EventBus()
    repo = InMemoryCheckpointRepository()
    manager = RecoveryManager(repository=repo, event_bus=bus)
    
    with pytest.raises(RecoveryError):
        manager.recover()
        
    manager.create_checkpoint(portfolio_version=5, event_sequence=100)
    
    recovered = manager.recover()
    assert recovered.portfolio_version == 5
    assert recovered.event_sequence == 100
