from tradiba.hermes.portfolio.learning.portfolio_learning import PortfolioLearningEngine

def test_portfolio_learning():
    engine = PortfolioLearningEngine({})
    
    # Record some outcomes
    engine.record_outcome({"regime": "bull", "pnl": 0.05})
    engine.record_outcome({"regime": "bull", "pnl": 0.03})
    engine.record_outcome({"regime": "bear", "pnl": -0.02})
    
    learned = engine.learn_from_history()
    
    # Bull average pnl is positive (+0.04), so multiplier should be > 1.0
    assert learned["bull"]["allocation_multiplier"] > 1.0
    
    # Bear average pnl is negative (-0.02), so multiplier should be < 1.0
    assert learned["bear"]["allocation_multiplier"] < 1.0
