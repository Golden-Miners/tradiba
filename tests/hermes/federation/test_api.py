from tradiba.hermes.federation.api.endpoints import FederationEndpoints

def test_api():
    api = FederationEndpoints()
    assert api.handle_connect({"node_id": "n1"})["node"] == "n1"
    assert api.handle_discover("cap1")["available"]
    assert api.handle_workflow("wf1")["status"] == "started"
    assert api.handle_exchange({})["status"] == "exchanged"
