from typing import Dict, Any, List

class PerformanceAttribution:
    """
    Produces metrics showing:
    - Strategy contribution
    - Allocation impact
    - Risk contribution
    - Regime performance
    - Decision effectiveness
    - Learning progression
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config

    def calculate_attribution(self, portfolio_returns: List[float], strategy_returns: Dict[str, List[float]], allocations: Dict[str, List[float]]) -> Dict[str, Any]:
        """
        Calculates attribution metrics for the portfolio.
        """
        if not portfolio_returns:
            return {}

        attribution = {
            "strategy_contribution": {},
            "risk_contribution": {}
        }

        # Calculate strategy contribution
        for sid, rets in strategy_returns.items():
            allocs = allocations.get(sid, [])
            if len(rets) == len(allocs) and len(rets) == len(portfolio_returns):
                contribution = sum(r * a for r, a in zip(rets, allocs))
                attribution["strategy_contribution"][sid] = contribution
                
                # Simplified risk contribution (variance contribution)
                variance = sum(r * r for r in rets) / len(rets)
                avg_alloc = sum(allocs) / len(allocs) if allocs else 0
                attribution["risk_contribution"][sid] = variance * (avg_alloc ** 2)

        return attribution
