from typing import Dict

class EcosystemGovernance:
    """
    Governs access to core API endpoints, data access, and ecosystem resources.
    """
    def __init__(self):
        self.policies: Dict[str, bool] = {"allow_external_network": False}

    def check_compliance(self, app_id: str, action: str) -> bool:
        if action == "network_access":
            return self.policies["allow_external_network"]
        return True
