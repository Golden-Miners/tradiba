import pytest
import time
from tradiba.resilience.circuit_breaker import CircuitBreaker, CircuitState
from tradiba.resilience.configuration import CircuitBreakerConfig
from tradiba.resilience.exceptions import CircuitBreakerOpenError

def test_circuit_breaker_transitions():
    config = CircuitBreakerConfig(failure_threshold=2, recovery_timeout_seconds=0.1)
    cb = CircuitBreaker("test_cb", config)
    
    def fail_op():
        raise ValueError("Failed!")
        
    def success_op():
        return "Success!"
        
    assert cb.state == CircuitState.CLOSED
    
    # First failure
    with pytest.raises(ValueError):
        cb.call(fail_op)
    assert cb.state == CircuitState.CLOSED
    
    # Second failure triggers OPEN
    with pytest.raises(ValueError):
        cb.call(fail_op)
    assert cb.state == CircuitState.OPEN
    
    # Third call fails fast
    with pytest.raises(CircuitBreakerOpenError):
        cb.call(success_op)
        
    # Wait for recovery timeout
    time.sleep(0.2)
    
    # Call should succeed and transition to CLOSED
    result = cb.call(success_op)
    assert result == "Success!"
    assert cb.state == CircuitState.CLOSED
