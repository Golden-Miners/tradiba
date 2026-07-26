def test_scoring():
    """Verify that scoring deterministically produces a normalized composite score."""
    from tradiba.intelligence.scoring import StandardScoringEngine
    engine = StandardScoringEngine()
    scorecard = engine.score_strategy("strat_1", {"cagr": 0.2, "sharpe_ratio": 1.5, "max_drawdown": 0.1})
    assert scorecard.composite_score == 0.5
