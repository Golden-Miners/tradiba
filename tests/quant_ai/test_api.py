from tradiba.quant_ai.api.endpoints import QuantAIEndpoints

def test_api():
    api = QuantAIEndpoints()
    assert api.handle_forecast({})["status"] == "success"
