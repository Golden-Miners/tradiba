class DistributedError(Exception):
    """Base exception for all distributed operations."""
    pass

class RetryableError(DistributedError):
    """
    Raised when an operation failed due to a transient condition (e.g., network timeout)
    and should be retried.
    """
    pass

class FatalError(DistributedError):
    """
    Raised when an operation failed due to a terminal condition (e.g., validation error,
    fatal misconfiguration) and should NOT be retried.
    """
    pass

class LeaseLostError(DistributedError):
    """Raised when a node loses its lease while performing a leader action."""
    pass

class LockAcquisitionError(DistributedError):
    """Raised when a distributed lock cannot be acquired within the timeout."""
    pass
