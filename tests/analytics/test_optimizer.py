from tradiba.analytics.optimization import MaxSharpeOptimizer
from tradiba.analytics.portfolio import PortfolioSnapshot
from datetime import datetime
from decimal import Decimal

def test_optimization():
    snapshot = PortfolioSnapshot(
        timestamp=datetime.now(),
        equity=Decimal("10000"),
        cash=Decimal("5000"),
        positions=(),
        accounts=(),
        currency="USD"
    )
    
    optimizer = MaxSharpeOptimizer()
    target_weights = optimizer.optimize(snapshot, constraints={})
    
    assert target_weights["strategy_1"] == 0.6
    assert target_weights["strategy_2"] == 0.4
