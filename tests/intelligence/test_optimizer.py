def test_optimizer():
    """Verify optimizer logic."""
    from tradiba.intelligence.optimizer import VolatilityTargetingAllocator
    from tradiba.intelligence.scoring import StrategyScorecard
    
    scorecards = [
        StrategyScorecard("strat_1", 0, 0, 0, 500, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        StrategyScorecard("strat_2", 0, 0, 0, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ]
    
    allocator = VolatilityTargetingAllocator()
    allocations = allocator.allocate(scorecards, total_capital=30000)
    
    assert allocations[0].strategy_id == "strat_1"
    assert allocations[0].capital == 20000
    assert allocations[1].strategy_id == "strat_2"
    assert allocations[1].capital == 10000
