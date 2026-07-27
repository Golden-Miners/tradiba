"""Reward Framework module."""

from typing import Dict, Any

class RewardFramework:
    """Evaluates candidates using configurable metrics."""

    def __init__(self, version: str = "v1") -> None:
        self.version = version

    def calculate_net_return(self, results: Dict[str, Any]) -> float:
        return results.get("net_return", 0.0)

    def calculate_sharpe_ratio(self, results: Dict[str, Any]) -> float:
        return results.get("sharpe_ratio", 0.0)

    def calculate_sortino_ratio(self, results: Dict[str, Any]) -> float:
        return results.get("sortino_ratio", 0.0)

    def calculate_max_drawdown(self, results: Dict[str, Any]) -> float:
        return results.get("max_drawdown", 0.0)

    def calculate_profit_factor(self, results: Dict[str, Any]) -> float:
        return results.get("profit_factor", 0.0)

    def calculate_win_rate(self, results: Dict[str, Any]) -> float:
        return results.get("win_rate", 0.0)

    def evaluate(self, results: Dict[str, Any]) -> Dict[str, float]:
        """Returns all metrics for a given strategy result."""
        return {
            "net_return": self.calculate_net_return(results),
            "sharpe_ratio": self.calculate_sharpe_ratio(results),
            "sortino_ratio": self.calculate_sortino_ratio(results),
            "max_drawdown": self.calculate_max_drawdown(results),
            "profit_factor": self.calculate_profit_factor(results),
            "win_rate": self.calculate_win_rate(results),
            "consistency": results.get("consistency", 1.0),
            "stability": results.get("stability", 1.0),
        }
