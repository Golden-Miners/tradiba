from typing import Dict, Any

class ExecutiveDecisionCockpit:
    """
    Provides dashboards for KPIs, forecasts, and scenario comparisons linked back to the Digital Brain.
    """
    def get_dashboard(self) -> Dict[str, Any]:
        return {"kpis": {"revenue": "up", "risk": "low"}}
