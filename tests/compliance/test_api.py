from tradiba.compliance.api.endpoints import ComplianceEndpoints

def test_api():
    api = ComplianceEndpoints()
    assert api.handle_rule({})["status"] == "success"
