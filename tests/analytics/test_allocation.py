from tradiba.analytics.allocation import AllocationEngine
from decimal import Decimal

def test_allocation():
    engine = AllocationEngine()
    
    strategies = ["strategy_1", "strategy_2"]
    weights = {"strategy_1": 0.6, "strategy_2": 0.4}
    total_capital = Decimal("10000")
    
    allocations = engine.allocate(strategies, weights, total_capital)
    
    assert allocations["strategy_1"] == Decimal("6000.0")
    assert allocations["strategy_2"] == Decimal("4000.0")
