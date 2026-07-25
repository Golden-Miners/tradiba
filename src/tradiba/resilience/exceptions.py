class ResilienceError(Exception):
    """Base exception for resilience failures."""
    pass

class CircuitBreakerOpenError(ResilienceError):
    """Raised when an operation is attempted but the circuit breaker is open."""
    pass

class RecoveryError(ResilienceError):
    """Raised when the system fails to recover from a checkpoint."""
    pass

class RateLimitExceededError(ResilienceError):
    """Raised when a request exceeds the defined rate limit."""
    pass

class ChaosInjectedError(ResilienceError):
    """Raised artificially by the chaos engineering framework."""
    pass
