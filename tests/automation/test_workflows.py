from tradiba.automation.workflows.engine import EnterpriseWorkflowEngine

def test_workflows():
    eng = EnterpriseWorkflowEngine()
    eng.register_workflow("w1", {})
    assert eng.execute_workflow("w1")
    assert not eng.execute_workflow("w2")
