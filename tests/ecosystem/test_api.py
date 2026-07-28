from tradiba.ecosystem.api.endpoints import EcosystemEndpoints

def test_api():
    api = EcosystemEndpoints()
    assert api.handle_install("app1")["status"] == "installed"
    assert api.handle_license({})["status"] == "licensed"
