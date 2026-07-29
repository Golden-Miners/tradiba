from tradiba.strategy.forecasting.platform import ForecastingPlatform

def test_forecasting():
    platform = ForecastingPlatform()
    res = platform.generate_forecast("revenue", 12)
    assert res["target"] == "revenue"
    assert res["horizon"] == 12
