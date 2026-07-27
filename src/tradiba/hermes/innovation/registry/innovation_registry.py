from typing import Dict, Any, List

class InnovationRegistry:
    """
    Maintains the lineage, audit history, and approval chain for all innovations.
    """
    def __init__(self):
        self.innovations: Dict[str, Dict[str, Any]] = {}
        
    def register(self, proposal_id: str, cap_type: str, details: Dict[str, Any]):
        self.innovations[proposal_id] = {
            "type": cap_type,
            "details": details,
            "status": "REGISTERED",
            "history": ["REGISTERED"]
        }
        
    def update_status(self, proposal_id: str, status: str):
        if proposal_id in self.innovations:
            self.innovations[proposal_id]["status"] = status
            self.innovations[proposal_id]["history"].append(status)
            
    def get_lineage(self, proposal_id: str) -> List[str]:
        return self.innovations.get(proposal_id, {}).get("history", [])
