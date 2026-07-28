from tradiba.automation.api.endpoints import AutomationEndpoints

def test_api():
    api = AutomationEndpoints()
    assert api.handle_run({})["status"] == "running"
    assert api.handle_approve("r1")["status"] == "approved"
