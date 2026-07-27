from typing import Dict, Any

class StrategicPlanningEngine:
    """
    Manages strategic objectives, initiatives, dependencies, and risks.
    """
    def __init__(self):
        self.objectives = {}
        
    def add_objective(self, obj_id: str, title: str):
        self.objectives[obj_id] = {"title": title, "status": "DRAFT"}
        
    def get_objective(self, obj_id: str) -> Dict[str, Any]:
        return self.objectives.get(obj_id, {})
