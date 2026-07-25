import pytest
from tradiba.analytics.expected_shortfall import ExpectedShortfall
from tradiba.analytics.portfolio import PortfolioSnapshot
from datetime import datetime
from decimal import Decimal

def test_expected_shortfall():
    snapshot = PortfolioSnapshot(
        timestamp=datetime.now(),
        equity=Decimal("10000"),
        cash=Decimal("5000"),
        positions=(),
        accounts=(),
        currency="USD"
    )
    
    es = ExpectedShortfall()
    result = es.calculate(snapshot)
    
    assert result["expected_shortfall"] == pytest.approx(700.0)
