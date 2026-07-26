from typing import List, Dict, Any
from tradiba.decision.models.decision import Decision, DecisionStatus

class DecisionAnalytics:
    """Calculates metrics around decision governance and processes."""
    
    def analyze_batch(self, decisions: List[Decision]) -> Dict[str, Any]:
        if not decisions:
            return {"approval_rate": 0.0, "average_confidence": 0.0}
            
        approved = sum(1 for d in decisions if d.status == DecisionStatus.APPROVED)
        total_conf = sum(d.confidence for d in decisions)
        
        return {
            "approval_rate": approved / len(decisions),
            "average_confidence": total_conf / len(decisions)
        }
