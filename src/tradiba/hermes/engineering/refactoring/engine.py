from typing import Dict, Any

class RefactoringEngine:
    """
    Proposes safe structural changes with rollback metadata.
    """
    def __init__(self):
        self.proposals = {}
        
    def propose(self, target: str, change: str) -> Dict[str, Any]:
        prop = {
            "target": target,
            "change": change,
            "rollback": f"Undo {change}"
        }
        self.proposals[target] = prop
        return prop
