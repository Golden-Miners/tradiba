class WorkflowExecutionError(Exception):
    """Raised when a workflow fails to execute properly."""

class ApprovalDeniedError(Exception):
    """Raised when a required approval is denied."""

class DependencyResolutionError(Exception):
    """Raised when a workflow step dependency cannot be resolved."""

class ConfigurationError(Exception):
    """Raised when workflow configuration is invalid."""

class InvalidStateTransitionError(Exception):
    """Raised when an invalid state transition is attempted."""
