class OptimizationError(Exception):
    """Base class for optimization exceptions."""
    pass

class SearchExhaustedError(OptimizationError):
    """Raised when a search algorithm can generate no more combinations."""
    pass
