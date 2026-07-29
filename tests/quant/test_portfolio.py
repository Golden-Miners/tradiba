from tradiba.quant.portfolio.construction import AdvancedPortfolioConstruction

def test_portfolio():
    construction = AdvancedPortfolioConstruction()
    weights = construction.optimize(["AAPL", "MSFT"], {})
    assert weights["AAPL"] == 0.5
