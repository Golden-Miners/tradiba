from tradiba.workflows.runbooks import RunbookExecutor, RunbookStep

def test_runbook_execution():
    executor = RunbookExecutor()
    
    context = {"called": False}
    def action():
        context["called"] = True
        return True
        
    executor.register_runbook("test", [RunbookStep("step1", action)])
    assert executor.execute("test") is True
    assert context["called"] is True
