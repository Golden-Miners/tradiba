from typing import Dict, Any, List

class CrossStrategyCoordinator:
    """
    Evaluates interactions between strategies to:
    - Reduce overlap
    - Diversify signals
    - Minimize conflicting positions
    - Improve overall portfolio efficiency
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.max_correlation = config.get("max_correlation", 0.70)

    def evaluate_interactions(
        self,
        strategies: List[Dict[str, Any]],
        correlation_matrix: Dict[str, Dict[str, float]]
    ) -> List[Dict[str, Any]]:
        """
        Filters out strategies that are too highly correlated with better performing ones.
        """
        if not strategies:
            return []

        # Sort strategies by a metric, e.g., sharpe ratio or ai_score
        sorted_strategies = sorted(
            strategies, 
            key=lambda s: s.get("sharpe", 0.0), 
            reverse=True
        )

        selected = []
        for s in sorted_strategies:
            # Check correlation with already selected strategies
            sid = s["id"]
            too_correlated = False
            for selected_s in selected:
                ssid = selected_s["id"]
                corr = correlation_matrix.get(sid, {}).get(ssid, 0.0)
                if corr > self.max_correlation:
                    too_correlated = True
                    break
            
            if not too_correlated:
                selected.append(s)

        return selected
