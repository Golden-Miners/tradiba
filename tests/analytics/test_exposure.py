from tradiba.analytics.exposure import ExposureAnalyzer
from tradiba.analytics.portfolio import PortfolioSnapshot
from datetime import datetime
from decimal import Decimal

def test_exposure_analyzer():
    snapshot = PortfolioSnapshot(
        timestamp=datetime.now(),
        equity=Decimal("10000"),
        cash=Decimal("5000"),
        positions=(
            {"symbol": "AAPL", "asset_class": "EQUITY", "notional_value": 3000.0, "currency": "USD"},
            {"symbol": "TSLA", "asset_class": "EQUITY", "notional_value": 2000.0, "currency": "USD"},
        ),
        accounts=(),
        currency="USD"
    )
    
    analyzer = ExposureAnalyzer(snapshot)
    
    sym_exp = analyzer.by_symbol()
    assert sym_exp["AAPL"] == 3000.0
    assert sym_exp["TSLA"] == 2000.0
    
    cls_exp = analyzer.by_asset_class()
    assert cls_exp["EQUITY"] == 5000.0
