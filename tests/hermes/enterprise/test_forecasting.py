from tradiba.hermes.enterprise.forecasting.predictive import PredictiveOperations

def test_forecasting():
    ops = PredictiveOperations()
    ops.add_forecast("incidents", 2.5)
    assert ops.forecasts["incidents"] == 2.5
