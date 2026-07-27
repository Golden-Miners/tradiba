from typing import Dict, Any, List

class ConsensusEngine:
    """
    Evaluates independent analysis and votes to form a collective recommendation.
    Supports policies: unanimous, majority.
    """
    def __init__(self, policy: str = "majority"):
        self.policy = policy
        
    def evaluate_votes(self, goal_id: str, votes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Takes a list of votes, e.g., [{"agent_id": "RiskAgent", "vote": "APPROVE"}, ...]
        Returns the consensus result.
        """
        if not votes:
            return {"status": "REJECTED", "reason": "NO_VOTES"}

        approve_count = sum(1 for v in votes if v.get("vote") == "APPROVE")
        reject_count = sum(1 for v in votes if v.get("vote") == "REJECT")
        
        if self.policy == "unanimous":
            if reject_count > 0:
                return {"status": "REJECTED", "reason": "NOT_UNANIMOUS"}
            return {"status": "APPROVED", "reason": "UNANIMOUS_APPROVAL"}
            
        elif self.policy == "majority":
            if approve_count > reject_count:
                return {"status": "APPROVED", "reason": "MAJORITY_APPROVAL"}
            else:
                return {"status": "REJECTED", "reason": "MAJORITY_REJECTION"}
                
        return {"status": "REJECTED", "reason": "UNKNOWN_POLICY"}
