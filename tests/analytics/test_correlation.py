from tradiba.analytics.correlation import CorrelationEngine

def test_correlation_engine():
    data = {
        "AAPL": [0.01, -0.02, 0.03],
        "TSLA": [0.02, -0.01, 0.01]
    }
    engine = CorrelationEngine(data)
    
    matrix = engine.correlation_matrix()
    assert matrix["AAPL"]["AAPL"] == 1.0
    assert matrix["TSLA"]["TSLA"] == 1.0
    
    clusters = engine.cluster_assets(n_clusters=2)
    assert "AAPL" in clusters
    assert "TSLA" in clusters
