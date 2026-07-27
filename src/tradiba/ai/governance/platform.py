
class AIGovernancePlatform:
    """
    Unified policy enforcement, audit logging, and approvals.
    """
    def __init__(self):
        self.audit_log = []
        
    def enforce_policy(self, user_role: str, action: str) -> bool:
        allowed = user_role in ["ADMIN", "MANAGER"] or action == "READ"
        self.audit_log.append(f"Action {action} by {user_role}: {'ALLOWED' if allowed else 'DENIED'}")
        return allowed
        
    def get_audit_trail(self):
        return self.audit_log
