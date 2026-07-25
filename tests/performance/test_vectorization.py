from tradiba.performance.vectorization import VectorizedAnalytics

def test_calculate_returns():
    prices = [100.0, 105.0, 102.9]
    returns = VectorizedAnalytics.calculate_returns(prices)
    
    assert len(returns) == 2
    assert abs(returns[0] - 0.05) < 1e-6
    assert abs(returns[1] - (-0.02)) < 1e-6

def test_rolling_volatility():
    import random
    random.seed(42)
    returns = [random.uniform(-0.02, 0.02) for _ in range(50)]
    
    vols = VectorizedAnalytics.rolling_volatility(returns, window=20)
    assert len(vols) == 31
    for v in vols:
        assert v >= 0
