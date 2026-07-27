from typing import Dict, Any

class HierarchicalPlanner:
    """
    Decomposes Missions -> Objectives -> Projects -> Tasks -> Actions.
    Supports pausing and reprioritization.
    """
    def __init__(self):
        self.active_plans: Dict[str, Dict[str, Any]] = {}
        
    def create_plan(self, mission_id: str, mission_goal: str) -> str:
        self.active_plans[mission_id] = {
            "mission": mission_goal,
            "objectives": [],
            "status": "ACTIVE"
        }
        return mission_id
        
    def add_objective(self, mission_id: str, objective: str):
        if mission_id in self.active_plans:
            self.active_plans[mission_id]["objectives"].append({
                "objective": objective,
                "status": "PENDING"
            })
            
    def pause_plan(self, mission_id: str):
        if mission_id in self.active_plans:
            self.active_plans[mission_id]["status"] = "PAUSED"
            
    def resume_plan(self, mission_id: str):
        if mission_id in self.active_plans:
            self.active_plans[mission_id]["status"] = "ACTIVE"
