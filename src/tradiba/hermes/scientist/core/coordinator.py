from typing import List

class AIScientistCore:
    """
    Coordinates the research lifecycle.
    """
    def __init__(self):
        self.active_investigations: List[str] = []
        
    def start_investigation(self, investigation_id: str):
        self.active_investigations.append(investigation_id)
        
    def get_investigations(self) -> List[str]:
        return self.active_investigations
