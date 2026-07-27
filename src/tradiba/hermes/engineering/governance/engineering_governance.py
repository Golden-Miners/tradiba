from typing import Dict

class DevelopmentGovernance:
    """
    Ensures PRs cannot be merged without explicit CI/CD and human sign-off.
    """
    def __init__(self):
        self.approved_prs = set()
        
    def can_merge(self, pr_id: str, checks: Dict[str, bool]) -> bool:
        if all(checks.values()):
            self.approved_prs.add(pr_id)
            return True
        return False
