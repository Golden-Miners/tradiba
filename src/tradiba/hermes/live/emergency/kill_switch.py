class KillSwitch:
    """
    Provides immediate platform-wide or scoped disablement of Hermes autonomy.
    Implemented as a fast in-memory toggle.
    """

    def __init__(self):
        self._global_kill = False
        self._scoped_kills = set() # Store scopes like 'tenant:123', 'strategy:alpha'

    def activate_global(self):
        self._global_kill = True

    def deactivate_global(self):
        self._global_kill = False

    def activate_scoped(self, scope: str):
        self._scoped_kills.add(scope)

    def deactivate_scoped(self, scope: str):
        self._scoped_kills.discard(scope)

    def is_killed(self, scopes: list[str] | None = None) -> bool:
        """
        Returns True if the system is killed globally, or if any of the provided scopes are killed.
        """
        if self._global_kill:
            return True
            
        if scopes:
            for scope in scopes:
                if scope in self._scoped_kills:
                    return True
                    
        return False
