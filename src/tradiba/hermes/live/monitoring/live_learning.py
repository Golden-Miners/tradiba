from typing import Dict, Any, List

class LiveLearningFeedback:
    """
    Collects execution feedback:
    - Executed trades
    - Execution quality (slippage, etc)
    - Policy violations
    - Operator feedback
    
    Learning updates future recommendations but does not change production policies automatically.
    """

    def __init__(self):
        self.trade_history: List[Dict[str, Any]] = []
        self.violation_history: List[Dict[str, Any]] = []

    def record_trade(self, trade_data: Dict[str, Any]):
        self.trade_history.append(trade_data)

    def record_violation(self, violation_data: Dict[str, Any]):
        self.violation_history.append(violation_data)

    def analyze_feedback(self) -> Dict[str, Any]:
        """
        Analyzes the collected feedback to improve future recommendations.
        """
        total_slippage = sum(t.get("slippage", 0.0) for t in self.trade_history)
        avg_slippage = total_slippage / len(self.trade_history) if self.trade_history else 0.0
        
        return {
            "trades_analyzed": len(self.trade_history),
            "average_slippage": avg_slippage,
            "total_violations": len(self.violation_history)
        }
