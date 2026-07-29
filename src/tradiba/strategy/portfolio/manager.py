from typing import Dict, Any, List

class StrategyPortfolioManager:
    """
    Manages strategic initiatives as a portfolio.
    """
    def __init__(self):
        self.portfolio: List[Dict[str, Any]] = []

    def add_initiative(self, initiative: Dict[str, Any]) -> None:
        self.portfolio.append(initiative)

    def get_portfolio(self) -> List[Dict[str, Any]]:
        return self.portfolio
