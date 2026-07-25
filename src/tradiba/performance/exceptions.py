class PerformanceError(Exception):
    """Base exception for performance engineering framework."""
    pass

class RegressionError(PerformanceError):
    """Raised when a performance benchmark falls outside acceptable baselines."""
    pass

class CapacityExceededError(PerformanceError):
    """Raised during capacity tests if the system cannot sustain the target load."""
    pass

class ComputeBackendError(PerformanceError):
    """Raised when the requested compute backend (e.g. GPU) is unavailable or fails."""
    pass
