def test_ranking():
    """Verify that strategy rankings are reproducible from identical inputs."""
    from tradiba.intelligence.ranking import WeightedRanker
    from tradiba.intelligence.scoring import StrategyScorecard
    
    scorecards = [
        StrategyScorecard("strat_1", 0.1, 0, 0, 0, 1.0, 0, 0, 0, 0, 0, 0, 0, 0.5),
        StrategyScorecard("strat_2", 0.1, 0, 0, 0, 2.0, 0, 0, 0, 0, 0, 0, 0, 0.8),
    ]
    
    ranker = WeightedRanker(weights={"composite_score": 1.0})
    ranked = ranker.rank(scorecards)
    
    assert ranked[0].strategy_id == "strat_2"
    assert ranked[1].strategy_id == "strat_1"
