
class OKRPlatform:
    """
    Tracks Objectives, Key Results, progress, and confidence.
    """
    def __init__(self):
        self.okrs = {}
        
    def add_okr(self, okr_id: str, objective: str):
        self.okrs[okr_id] = {"objective": objective, "progress": 0.0}
        
    def update_progress(self, okr_id: str, progress: float):
        if okr_id in self.okrs:
            self.okrs[okr_id]["progress"] = progress
