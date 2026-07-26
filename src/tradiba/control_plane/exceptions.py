class ControlPlaneError(Exception):
    """Base exception for Control Plane operations."""
    pass

class ConfigurationConflictError(ControlPlaneError):
    """Raised when configuration values conflict in an unresolvable way."""
    pass

class PolicyViolationError(ControlPlaneError):
    """Raised when a deployment violates an active operational policy."""
    pass

class AgentConnectionError(ControlPlaneError):
    """Raised when a Tradiba Agent cannot communicate with the control plane."""
    pass
