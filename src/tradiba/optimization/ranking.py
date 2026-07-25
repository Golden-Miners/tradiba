from abc import ABC, abstractmethod
from typing import List

from .metrics import OptimizationResult


class RankingStrategy(ABC):
    """Base interface for ranking optimization results."""
    
    @abstractmethod
    def score(self, result: OptimizationResult) -> float:
        """Calculates a score for a single result. Higher is better."""
        pass

    def rank(self, results: List[OptimizationResult]) -> List[OptimizationResult]:
        """Scores and sorts the results in descending order."""
        for r in results:
            r.score = self.score(r)
        return sorted(results, key=lambda x: x.score, reverse=True)


class ObjectiveRankingStrategy(RankingStrategy):
    """Ranks results based on a specific statistic field."""

    def __init__(self, objective_field: str):
        self.objective_field = objective_field

    def score(self, result: OptimizationResult) -> float:
        # Default to 0.0 if the field is missing
        return getattr(result.statistics, self.objective_field, 0.0)


class CompositeRankingStrategy(RankingStrategy):
    """Ranks results based on a custom composite formula."""
    
    def score(self, result: OptimizationResult) -> float:
        stats = result.statistics
        # Example: Net Profit * Win Rate / (Max Drawdown + 1)
        if stats.max_drawdown <= 0:
            return stats.net_profit * stats.win_rate
        return (stats.net_profit * stats.win_rate) / stats.max_drawdown
