from typing import Dict, Any

class TrustManager:
    """
    Mutual authentication and trust relationship evaluation.
    """
    def __init__(self):
        self.trusted_orgs: Dict[str, Dict[str, Any]] = {}

    def establish_trust(self, org_id: str, policies: Dict[str, Any]) -> bool:
        self.trusted_orgs[org_id] = policies
        return True

    def revoke_trust(self, org_id: str) -> bool:
        if org_id in self.trusted_orgs:
            del self.trusted_orgs[org_id]
            return True
        return False

    def evaluate_request(self, org_id: str, action: str) -> bool:
        if org_id not in self.trusted_orgs:
            return False
        return action in self.trusted_orgs[org_id].get("allowed_actions", [])
