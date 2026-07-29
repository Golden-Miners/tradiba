from tradiba.quant_ai.forecasting.probabilistic import ProbabilisticForecastingPlatform

def test_forecasting():
    platform = ProbabilisticForecastingPlatform()
    res = platform.generate_forecast("AAPL")
    assert res["symbol"] == "AAPL"
    assert res["expected_return"] == 0.05
