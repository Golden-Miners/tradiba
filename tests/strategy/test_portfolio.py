from tradiba.strategy.portfolio.manager import StrategyPortfolioManager

def test_portfolio():
    manager = StrategyPortfolioManager()
    manager.add_initiative({"id": "i1"})
    assert len(manager.get_portfolio()) == 1
