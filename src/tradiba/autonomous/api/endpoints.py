from typing import Dict, Any

class AutonomousEndpoints:
    """
    Exposes the REST endpoints.
    """
    def handle_create_mission(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "created", "mission_id": "m1"}

    def handle_plan(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {"status": "planned"}
