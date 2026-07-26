class IntelligenceError(Exception):
    """Base exception for the intelligence domain."""
    pass

class AllocationConstraintError(IntelligenceError):
    """Raised when an allocation violates risk or capacity constraints."""
    pass

class GovernanceRejectionError(IntelligenceError):
    """Raised when a strategy fails to pass a governance gate."""
    pass
