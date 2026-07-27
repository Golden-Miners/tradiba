from tradiba.hermes.portfolio.optimizer.risk_budget import RiskBudgetOptimizer

def test_concentration_limit():
    optimizer = RiskBudgetOptimizer({"max_concentration": 0.20})
    proposal = {"s1": 0.50, "s2": 0.10}
    meta = {"s1": {"sector": "tech"}, "s2": {"sector": "finance"}}
    
    optimized = optimizer.optimize(proposal, meta)
    assert optimized["s1"] == 0.20
    assert optimized["s2"] == 0.10

def test_sector_exposure_limit():
    optimizer = RiskBudgetOptimizer({"max_sector_exposure": 0.30, "max_concentration": 0.50})
    proposal = {"s1": 0.20, "s2": 0.20} # total tech = 0.40
    meta = {"s1": {"sector": "tech"}, "s2": {"sector": "tech"}}
    
    optimized = optimizer.optimize(proposal, meta)
    # Scale = 0.30 / 0.40 = 0.75
    # s1 = 0.20 * 0.75 = 0.15
    assert abs(optimized["s1"] - 0.15) < 0.01
    assert abs(optimized["s2"] - 0.15) < 0.01

def test_max_leverage_limit():
    optimizer = RiskBudgetOptimizer({"max_leverage": 1.0, "max_concentration": 1.0, "max_sector_exposure": 1.0})
    proposal = {"s1": 0.60, "s2": 0.60} # total = 1.20
    meta = {"s1": {"sector": "tech"}, "s2": {"sector": "finance"}}
    
    optimized = optimizer.optimize(proposal, meta)
    # Scale = 1.0 / 1.2 = 0.833
    assert abs(optimized["s1"] - 0.50) < 0.01
    assert abs(optimized["s2"] - 0.50) < 0.01
