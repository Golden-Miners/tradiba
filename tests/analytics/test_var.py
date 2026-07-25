from tradiba.analytics.var import HistoricalVaR
from tradiba.analytics.portfolio import PortfolioSnapshot
from datetime import datetime
from decimal import Decimal

def test_var():
    snapshot = PortfolioSnapshot(
        timestamp=datetime.now(),
        equity=Decimal("10000"),
        cash=Decimal("5000"),
        positions=(),
        accounts=(),
        currency="USD"
    )
    
    var_model = HistoricalVaR()
    result = var_model.calculate(snapshot)
    
    assert result["method"] == "historical"
    assert result["var_value"] == 500.0
