from tradiba.automation.orchestration.process_engine import ProcessOrchestrator

def test_orchestration():
    orch = ProcessOrchestrator()
    assert orch.start_process("p1")
    assert orch.rollback_process("p1")
    assert not orch.rollback_process("p2")
