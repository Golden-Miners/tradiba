from typing import Dict

class FederatedIdentity:
    """
    Organization, node, and agent identity management.
    """
    def __init__(self, org_id: str, node_id: str):
        self.org_id = org_id
        self.node_id = node_id
        self.certificates: Dict[str, str] = {}

    def get_identity(self) -> Dict[str, str]:
        return {"org_id": self.org_id, "node_id": self.node_id}

    def register_certificate(self, target_org: str, cert: str) -> None:
        self.certificates[target_org] = cert
