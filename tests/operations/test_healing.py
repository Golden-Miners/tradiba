from tradiba.operations.healing.orchestrator import SelfHealingOrchestrator

def test_healing():
    orch = SelfHealingOrchestrator()
    assert orch.execute_recovery("restart")
    assert not orch.execute_recovery("unknown")
