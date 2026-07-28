from tradiba.operations.api.endpoints import OperationsEndpoints

def test_api():
    api = OperationsEndpoints()
    assert api.handle_incident({})["status"] == "incident_logged"
    assert api.handle_heal({})["status"] == "healing_started"
