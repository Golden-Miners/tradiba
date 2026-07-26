from typing import List, Protocol, Dict, Optional
from tradiba.intelligence.scoring import StrategyScorecard

class RankerProtocol(Protocol):
    """Protocol for ranking a list of scored strategies."""
    
    def rank(self, scorecards: List[StrategyScorecard]) -> List[StrategyScorecard]:
        """Returns the strategies sorted by rank, best to worst."""
        ...

class WeightedRanker:
    """
    Reference Implementation: Configurable Weighted Ranker.
    Ranks strategies based on customizable weights applied to the scorecard.
    """
    
    def __init__(self, weights: Optional[Dict[str, float]] = None):
        if weights is None:
            self.weights: Dict[str, float] = {
                "composite_score": 0.5,
                "sharpe_ratio": 0.2,
                "max_drawdown": -0.1,  # Negative weight for penalties
                "cagr": 0.2
            }
        else:
            self.weights = weights
            
    def rank(self, scorecards: List[StrategyScorecard]) -> List[StrategyScorecard]:
        def calculate_score(card: StrategyScorecard) -> float:
            score = 0.0
            for metric, weight in self.weights.items():
                val = getattr(card, metric, 0.0)
                score += (val * weight)
            return score
            
        return sorted(scorecards, key=calculate_score, reverse=True)
