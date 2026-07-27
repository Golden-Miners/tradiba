from typing import List

class CrossTeamCoordinator:
    """
    Tracks blockers, dependencies, and deliverables.
    """
    def __init__(self):
        self.blockers = []
        
    def add_blocker(self, blocker: str):
        self.blockers.append(blocker)
        
    def get_blockers(self) -> List[str]:
        return self.blockers
