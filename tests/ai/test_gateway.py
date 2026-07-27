import pytest
from tradiba.ai.gateway.api import AIGateway

def test_gateway():
    gw = AIGateway()
    res = gw.route_request("valid_token", {"q": "hi"})
    assert res["status"] == "routed"
    
    with pytest.raises(PermissionError):
        gw.route_request("invalid", {"q": "hi"})
