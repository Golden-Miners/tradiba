from tradiba.strategy.api.endpoints import StrategyEndpoints

def test_api():
    api = StrategyEndpoints()
    assert api.handle_plan({})["status"] == "created"
    assert api.handle_forecast({})["status"] == "generated"
