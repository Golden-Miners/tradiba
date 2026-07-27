from typing import Dict, Any, List

class PlanOptimizer:
    """
    Optimizes adaptive plans across multiple dimensions: risk-adjusted return, capital efficiency, etc.
    """
    def __init__(self):
        pass
        
    def optimize(self, plans: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank and optimize a list of candidate plans.
        Returns the sorted list with best plans first.
        """
        if not plans:
            return []
            
        def evaluate_plan(plan: Dict[str, Any]) -> float:
            score = 100.0
            
            # Penalize high risk
            risk = plan.get("risk_score", 0.5)
            score -= (risk * 20)
            
            # Reward efficiency
            efficiency = plan.get("capital_efficiency", 0.5)
            score += (efficiency * 20)
            
            return score
            
        sorted_plans = sorted(plans, key=evaluate_plan, reverse=True)
        return sorted_plans
