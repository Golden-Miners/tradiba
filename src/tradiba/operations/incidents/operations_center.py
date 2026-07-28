from typing import Dict, Any

class OperationsCenter:
    """
    Unified operational control plane, dashboard state, global health monitoring.
    """
    def __init__(self):
        self.health: Dict[str, str] = {"status": "healthy"}

    def get_dashboard(self) -> Dict[str, Any]:
        return {"health": self.health, "active_incidents": []}
