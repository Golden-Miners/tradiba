from typing import List

class UnifiedPlanningEngine:
    """
    Supports hierarchical planning from Mission -> Tool.
    """
    def __init__(self):
        self.plans = {}
        
    def create_plan(self, plan_id: str, levels: List[str]):
        self.plans[plan_id] = {"levels": levels, "status": "DRAFT"}
        
    def execute_plan(self, plan_id: str) -> bool:
        if plan_id in self.plans:
            self.plans[plan_id]["status"] = "EXECUTING"
            return True
        return False
