from tradiba.hermes.portfolio.supervisor.cross_strategy import CrossStrategyCoordinator

def test_supervisor_filters_correlated_strategies():
    coordinator = CrossStrategyCoordinator({"max_correlation": 0.70})
    strategies = [
        {"id": "s1", "sharpe": 2.0},
        {"id": "s2", "sharpe": 1.5},
        {"id": "s3", "sharpe": 1.0}
    ]
    # s2 is highly correlated with s1. s3 is not.
    correlation_matrix = {
        "s2": {"s1": 0.80},
        "s3": {"s1": 0.10, "s2": 0.20}
    }
    
    selected = coordinator.evaluate_interactions(strategies, correlation_matrix)
    ids = [s["id"] for s in selected]
    
    assert "s1" in ids
    assert "s2" not in ids # filtered out due to high correlation with s1
    assert "s3" in ids
