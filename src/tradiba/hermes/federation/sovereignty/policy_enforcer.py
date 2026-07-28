from typing import Dict, Any

class PolicyEnforcer:
    """
    Data residency, confidentiality, and export controls.
    """
    def enforce_policy(self, request: Dict[str, Any], policy: str) -> bool:
        if policy == "data_residency":
            return request.get("region") == "local"
        if policy == "export_control":
            return not request.get("contains_ip", False)
        return True
