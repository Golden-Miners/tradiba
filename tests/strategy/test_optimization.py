from tradiba.strategy.optimization.decision_engine import DecisionOptimizationEngine

def test_optimization():
    engine = DecisionOptimizationEngine()
    opts = [{"cost": 10}, {"cost": 20}]
    res = engine.optimize(opts, {})
    assert res["cost"] == 10
