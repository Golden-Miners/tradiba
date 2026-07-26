def test_monitoring():
    """Verify monitoring alerts."""
    from tradiba.intelligence.monitoring import ContinuousMonitor
    from tradiba.intelligence.models.strategy_descriptor import StrategyDescriptor
    
    monitor = ContinuousMonitor(draw_down_limit=0.10)
    strats = [StrategyDescriptor(f"strat_{i}", "test", "v1", "auth", "low", [], []) for i in (1,2)]
    
    metrics = {
        "strat_1": {"max_drawdown": 0.05},
        "strat_2": {"max_drawdown": 0.15},
    }
    
    flagged = monitor.check_health(strats, metrics)
    assert len(flagged) == 1
    assert flagged[0] == "strat_2"
