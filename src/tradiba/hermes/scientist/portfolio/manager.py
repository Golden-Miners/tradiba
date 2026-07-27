from typing import Dict, Any

class ResearchPortfolioManager:
    """
    Tracks active projects, completed studies, and research impact.
    """
    def __init__(self):
        self.projects: Dict[str, Dict[str, Any]] = {}
        
    def add_project(self, project_id: str, status: str = "ACTIVE"):
        self.projects[project_id] = {"status": status, "impact": 0.0}
        
    def complete_project(self, project_id: str, impact: float):
        if project_id in self.projects:
            self.projects[project_id]["status"] = "COMPLETED"
            self.projects[project_id]["impact"] = impact
