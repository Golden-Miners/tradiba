from typing import List, Dict, Any
from collections import Counter

class EnsembleDecisionEngine:
    """
    Reference Implementation: Ensemble Decision Engine.
    Aggregates signals from multiple live strategies to form a consensus.
    """
    
    def __init__(self, method: str = "majority_vote"):
        self.method = method
        
    def aggregate_signals(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Takes a list of strategy signals (e.g., {'strategy_id': 'X', 'action': 'BUY', 'confidence': 0.8})
        and returns an aggregated consensus signal.
        """
        if not signals:
            return {"action": "HOLD", "confidence": 0.0, "sources": 0}
            
        if self.method == "majority_vote":
            return self._majority_vote(signals)
        elif self.method == "confidence_weighted":
            return self._confidence_weighted(signals)
        else:
            raise ValueError(f"Unknown ensemble method: {self.method}")
            
    def _majority_vote(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        actions = [s.get("action", "HOLD") for s in signals]
        counter = Counter(actions)
        most_common_action, count = counter.most_common(1)[0]
        
        return {
            "action": most_common_action,
            "confidence": count / len(signals),
            "sources": len(signals)
        }
        
    def _confidence_weighted(self, signals: List[Dict[str, Any]]) -> Dict[str, Any]:
        action_weights = {"BUY": 0.0, "SELL": 0.0, "HOLD": 0.0}
        
        for s in signals:
            action = s.get("action", "HOLD")
            conf = s.get("confidence", 0.5)
            if action in action_weights:
                action_weights[action] += conf
                
        best_action = max(action_weights, key=lambda k: action_weights[k])
        total_weight = sum(action_weights.values())
        
        return {
            "action": best_action,
            "confidence": action_weights[best_action] / total_weight if total_weight > 0 else 0.0,
            "sources": len(signals)
        }
