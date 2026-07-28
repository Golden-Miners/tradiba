from typing import Dict, List, Set

class SkillSandboxIsolation:
    """
    Sandboxing rules for filesystem, network, secret management, memory/CPU limits.
    """
    def __init__(self):
        self.granted_permissions: Dict[str, Set[str]] = {}

    def grant_permissions(self, skill_id: str, permissions: List[str]) -> None:
        if skill_id not in self.granted_permissions:
            self.granted_permissions[skill_id] = set()
        self.granted_permissions[skill_id].update(permissions)

    def check_permission(self, skill_id: str, permission: str) -> bool:
        allowed = self.granted_permissions.get(skill_id, set())
        return permission in allowed or "all" in allowed
