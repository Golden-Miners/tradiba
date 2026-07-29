from typing import Dict, Any

class StrategicPlanningEngine:
    """
    Supports hierarchical planning across multiple horizons (Vision -> Tasks).
    """
    def __init__(self):
        self.plans: Dict[str, Dict[str, Any]] = {}

    def create_plan(self, plan_id: str, details: Dict[str, Any]) -> None:
        self.plans[plan_id] = details

    def get_plan(self, plan_id: str) -> Dict[str, Any]:
        return self.plans.get(plan_id, {})
