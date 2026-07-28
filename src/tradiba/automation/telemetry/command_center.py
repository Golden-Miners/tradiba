from typing import Dict, Any

class CommandCenter:
    """
    Metrics aggregation for the Operations Command Center dashboards.
    """
    def __init__(self):
        self.stats: Dict[str, Any] = {"active_workflows": 0, "failures": 0}

    def get_dashboard_metrics(self) -> Dict[str, Any]:
        return self.stats
