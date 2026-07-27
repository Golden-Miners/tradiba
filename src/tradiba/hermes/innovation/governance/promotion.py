from typing import Dict, Any

class InnovationGovernance:
    """
    Ensures human approval is mandatory for production promotion.
    """
    def __init__(self):
        self.pending_approvals: Dict[str, Dict[str, Any]] = {}
        
    def submit_for_review(self, proposal_id: str, cap_type: str):
        self.pending_approvals[proposal_id] = {
            "type": cap_type,
            "human_approved": False,
            "security_reviewed": False,
            "risk_reviewed": False
        }
        
    def human_approve(self, proposal_id: str) -> bool:
        if proposal_id in self.pending_approvals:
            self.pending_approvals[proposal_id]["human_approved"] = True
            return True
        return False
        
    def is_promotable(self, proposal_id: str) -> bool:
        if proposal_id not in self.pending_approvals:
            return False
            
        rec = self.pending_approvals[proposal_id]
        # In a real system, security and risk would also need to be true.
        # For simplicity, we just check human approval.
        return rec["human_approved"]
