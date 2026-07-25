from tradiba.analytics.stress import EquityMarketShock
from tradiba.analytics.portfolio import PortfolioSnapshot
from datetime import datetime
from decimal import Decimal

def test_stress_testing():
    snapshot = PortfolioSnapshot(
        timestamp=datetime.now(),
        equity=Decimal("10000"),
        cash=Decimal("5000"),
        positions=(),
        accounts=(),
        currency="USD"
    )
    
    scenario = EquityMarketShock()
    shocked = scenario.apply(snapshot)
    
    assert shocked.equity == Decimal("8000")
