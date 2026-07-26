import pytest
from tradiba.evolution.rollout import RollingUpgradeManager
from tradiba.evolution.rollback import RollbackOrchestrator
from tradiba.evolution.exceptions import RollbackFailedError

def test_rollback_orchestrator():
    rollout = RollingUpgradeManager()
    rollout.promote_to_production("web_ui", "v2")
    
    orchestrator = RollbackOrchestrator(rollout)
    orchestrator.register_safe_state("web_ui", "v1")
    
    orchestrator.trigger_rollback("web_ui", "health_check_failed")
    
    assert rollout.get_deployment_status("web_ui") == "v1"
    
    with pytest.raises(RollbackFailedError):
        orchestrator.trigger_rollback("unknown", "error")
