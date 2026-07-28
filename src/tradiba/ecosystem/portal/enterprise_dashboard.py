from typing import Dict, Any

class EnterprisePortal:
    """
    Backend services backing the Enterprise Operations portal.
    """
    def __init__(self):
        self.portal_stats: Dict[str, Any] = {"active_users": 0}

    def get_dashboard_data(self) -> Dict[str, Any]:
        return {"stats": self.portal_stats}
