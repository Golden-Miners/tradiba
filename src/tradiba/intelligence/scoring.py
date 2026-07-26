from dataclasses import dataclass
from typing import Dict, Protocol

@dataclass
class StrategyScorecard:
    strategy_id: str
    cagr: float
    cagr_stability: float
    max_drawdown: float
    var_95: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float
    walk_forward_stability: float
    slippage_bps: float
    fill_quality: float
    runtime_health: float
    error_rate: float
    
    # The normalized score (0.0 to 1.0)
    composite_score: float = 0.0

class ScoringEngine(Protocol):
    """Protocol for scoring strategies based on their historical and live performance."""
    
    def score_strategy(self, strategy_id: str, metrics: Dict[str, float]) -> StrategyScorecard:
        """Computes a normalized scorecard for the given strategy metrics."""
        ...

class StandardScoringEngine:
    """
    Reference Implementation: Standard Scoring Engine.
    Normalizes a dictionary of raw metrics into a composite score.
    """
    
    def score_strategy(self, strategy_id: str, metrics: Dict[str, float]) -> StrategyScorecard:
        # Mock normalization and scoring logic
        composite = min(1.0, max(0.0, metrics.get("sharpe_ratio", 0.0) / 3.0))
        
        return StrategyScorecard(
            strategy_id=strategy_id,
            cagr=metrics.get("cagr", 0.0),
            cagr_stability=metrics.get("cagr_stability", 0.0),
            max_drawdown=metrics.get("max_drawdown", 0.0),
            var_95=metrics.get("var_95", 0.0),
            sharpe_ratio=metrics.get("sharpe_ratio", 0.0),
            sortino_ratio=metrics.get("sortino_ratio", 0.0),
            calmar_ratio=metrics.get("calmar_ratio", 0.0),
            walk_forward_stability=metrics.get("walk_forward_stability", 0.0),
            slippage_bps=metrics.get("slippage_bps", 0.0),
            fill_quality=metrics.get("fill_quality", 0.0),
            runtime_health=metrics.get("runtime_health", 0.0),
            error_rate=metrics.get("error_rate", 0.0),
            composite_score=composite
        )
