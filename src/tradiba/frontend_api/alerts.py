from typing import Dict, Any, List

class AlertCenterService:
    """Aggregates and filters platform notifications."""
    
    def __init__(self) -> None:
        self._alerts: List[Dict[str, Any]] = []
        
    def push_alert(self, alert: Dict[str, Any]) -> None:
        self._alerts.append(alert)
        
    def get_alerts(self, severity: str | None = None) -> List[Dict[str, Any]]:
        if severity:
            return [a for a in self._alerts if a.get("severity") == severity]
        return self._alerts
