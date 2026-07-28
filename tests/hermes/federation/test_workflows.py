from tradiba.hermes.federation.workflows.federated_orchestrator import FederatedOrchestrator

def test_workflows():
    orch = FederatedOrchestrator()
    assert orch.start_workflow("wf1", "org2")
    assert orch.complete_workflow("wf1")
