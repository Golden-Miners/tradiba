from tradiba.operations.prediction.reliability_forecaster import ReliabilityForecaster

def test_prediction():
    forecaster = ReliabilityForecaster()
    res = forecaster.forecast("s1")
    assert res["service"] == "s1"
    assert "time_to_exhaustion" in res
