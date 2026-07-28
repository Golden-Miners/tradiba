from typing import Dict, Any, List
from tradiba.hermes.skills.sandbox.isolation import SkillSandboxIsolation

class SkillGovernanceEngine:
    """
    Skill execution governance validating permissions, policies, and audit logging.
    """
    def __init__(self, sandbox: SkillSandboxIsolation):
        self.sandbox = sandbox
        self.audit_logs: List[Dict[str, Any]] = []

    def validate_request(self, skill_id: str, required_permissions: List[str]) -> bool:
        for perm in required_permissions:
            if not self.sandbox.check_permission(skill_id, perm):
                self.audit_logs.append({
                    "skill_id": skill_id,
                    "status": "REJECTED",
                    "reason": f"Missing permission {perm}"
                })
                return False

        self.audit_logs.append({
            "skill_id": skill_id,
            "status": "APPROVED",
            "permissions": required_permissions
        })
        return True
