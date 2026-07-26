class AIOpsError(Exception):
    """Base class for AIOps layer exceptions."""
    pass

class PolicyViolationError(AIOpsError):
    """Raised when an AI recommendation violates safety policies."""
    pass
