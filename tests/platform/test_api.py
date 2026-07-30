from tradiba.platform.api.endpoints import PlatformEndpoints

def test_api():
    api = PlatformEndpoints()
    assert api.health()["status"] == "ok"
