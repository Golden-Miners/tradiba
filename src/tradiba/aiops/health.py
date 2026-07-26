from dataclasses import dataclass
from typing import Any

@dataclass(slots=True)
class StrategyHealthScore:
    overall: float
    risk: float
    execution: float
    stability: float
    confidence: float

class StrategyHealthEngine:
    """Calculates multidimensional health scores for active strategies."""
    def calculate_health(self, strategy_state: dict[str, Any]) -> StrategyHealthScore:
        # Dummy deterministic scoring based on inputs
        win_rate = strategy_state.get("win_rate", 0.5)
        error_count = strategy_state.get("errors", 0)
        
        risk = max(0.0, 1.0 - (strategy_state.get("risk_violations", 0) * 0.2))
        execution = max(0.0, 1.0 - (strategy_state.get("latency_ms", 10) / 100.0))
        stability = max(0.0, 1.0 - (error_count * 0.1))
        
        overall = (risk + execution + stability + win_rate) / 4.0
        confidence = 0.95 if strategy_state.get("uptime_hours", 0) > 24 else 0.5
        
        return StrategyHealthScore(
            overall=overall,
            risk=risk,
            execution=execution,
            stability=stability,
            confidence=confidence
        )
