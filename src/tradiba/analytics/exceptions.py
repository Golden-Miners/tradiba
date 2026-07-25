class AnalyticsError(Exception):
    """Base exception for analytics operations."""
    pass

class OptimizationError(AnalyticsError):
    """Raised when portfolio optimization fails to converge or constraints are unsatisfiable."""
    pass

class StressTestError(AnalyticsError):
    """Raised when a stress scenario cannot be applied."""
    pass

class AllocationError(AnalyticsError):
    """Raised when capital allocation policies fail."""
    pass
