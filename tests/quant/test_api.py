from tradiba.quant.api.endpoints import QuantEndpoints

def test_api():
    api = QuantEndpoints()
    assert api.handle_alpha({})["status"] == "success"
