from typing import Dict, Any

class PortfolioLearningEngine:
    """
    Learns from:
    - Allocation outcomes
    - Regime transitions
    - Paper-trading performance
    - Digital Twin simulations
    - Historical attribution
    
    Learning updates recommendation models but does not alter production portfolios.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.history = []

    def record_outcome(self, outcome: Dict[str, Any]):
        """
        Records the outcome of an allocation decision.
        """
        self.history.append(outcome)

    def learn_from_history(self) -> Dict[str, Any]:
        """
        Analyzes history to extract lessons for future allocations.
        Returns a dictionary of learned parameters.
        """
        if not self.history:
            return {}

        # Simple learning: identify which regimes have been most profitable
        regime_performance = {}
        for outcome in self.history:
            regime = outcome.get("regime", "unknown")
            pnl = outcome.get("pnl", 0.0)
            if regime not in regime_performance:
                regime_performance[regime] = []
            regime_performance[regime].append(pnl)

        learned_params = {}
        for regime, pnls in regime_performance.items():
            avg_pnl = sum(pnls) / len(pnls)
            # If a regime consistently loses money, reduce allocation multiplier
            multiplier = 1.0
            if avg_pnl < 0:
                multiplier = max(0.1, 1.0 + avg_pnl) # reduce multiplier
            elif avg_pnl > 0:
                multiplier = min(2.0, 1.0 + avg_pnl) # increase multiplier
                
            learned_params[regime] = {"allocation_multiplier": multiplier}

        return learned_params
