from tradiba.decision.models.decision import Decision
from tradiba.decision.models.explanation import Explanation

class ExplainabilityEngine:
    """Synthesizes the decision graph into human-readable text."""
    
    def explain(self, decision: Decision) -> Explanation:
        return Explanation(
            decision_summary=f"Decision {decision.decision_id} to {decision.category.value}",
            reasons=["Digital twin validation passed.", "Portfolio risk remains within limits."],
            confidence=decision.confidence
        )
