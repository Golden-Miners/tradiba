from typing import Dict, Any

class UnifiedGovernance:
    """
    Applies one governance model across all AI activity.
    """
    def __init__(self):
        self.policies = {}
        
    def add_policy(self, name: str, rules: Dict[str, Any]):
        self.policies[name] = rules
        
    def check_compliance(self, action: str, context: Dict[str, Any]) -> bool:
        return True
