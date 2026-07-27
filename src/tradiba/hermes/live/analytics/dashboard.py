from typing import Dict, Any, List

class AutonomousOperationsDashboard:
    """
    Data aggregation layer for the UI.
    Provides current status, active goals, policy violations, etc.
    """

    def __init__(self):
        self.status = "ONLINE"
        self.active_goals: List[str] = []
        self.open_positions: List[Dict[str, Any]] = []
        self.policy_violations: List[Dict[str, Any]] = []
        self.safety_alerts: List[str] = []

    def get_summary(self, 
                    autonomy_level: int, 
                    killed: bool, 
                    paused: bool) -> Dict[str, Any]:
        return {
            "status": "KILLED" if killed else ("PAUSED" if paused else self.status),
            "autonomy_level": autonomy_level,
            "active_goals": len(self.active_goals),
            "open_positions": len(self.open_positions),
            "recent_violations": len(self.policy_violations),
            "recent_alerts": len(self.safety_alerts)
        }
