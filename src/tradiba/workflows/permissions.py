class PermissionService:
    """Validates roles for operations."""
    def __init__(self) -> None:
        self._roles: dict[str, list[str]] = {}
        
    def assign_role(self, user: str, role: str) -> None:
        if user not in self._roles:
            self._roles[user] = []
        self._roles[user].append(role)
        
    def has_role(self, user: str, role: str) -> bool:
        return role in self._roles.get(user, [])
