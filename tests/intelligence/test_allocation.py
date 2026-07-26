def test_allocation():
    """Verify that allocation algorithms respect configured constraints."""
    from tradiba.intelligence.allocation import CapitalAllocationEngine
    from tradiba.intelligence.optimizer import EqualWeightAllocator
    from tradiba.intelligence.scoring import StrategyScorecard
    
    scorecards = [
        StrategyScorecard("strat_1", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        StrategyScorecard("strat_2", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
    ]
    
    engine = CapitalAllocationEngine(EqualWeightAllocator())
    allocations = engine.rebalance(scorecards, total_capital=100000)
    
    assert len(allocations) == 2
    assert allocations[0].capital == 50000
    assert allocations[1].target_weight == 0.5
