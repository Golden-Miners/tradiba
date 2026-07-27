from typing import List

class CognitiveGovernance:
    """
    Asserts permission checks and policy bounds before executing any cognitive plan or skill.
    """
    def __init__(self, global_policies: List[str]):
        self.policies = global_policies
        
    def evaluate_skill_execution(self, skill_name: str, requested_permissions: List[str]) -> bool:
        """
        Validates if a skill is allowed to execute based on its requested permissions.
        """
        for perm in requested_permissions:
            if perm not in self.policies:
                return False
        return True
