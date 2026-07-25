import time
from enum import Enum, auto
from typing import Callable, Any
from tradiba.resilience.configuration import CircuitBreakerConfig
from tradiba.resilience.exceptions import CircuitBreakerOpenError
from tradiba.events import EventBus
from tradiba.resilience.events import CircuitOpenedEvent, CircuitClosedEvent
import logging

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = auto()
    OPEN = auto()
    HALF_OPEN = auto()

class CircuitBreaker:
    """
    Prevents execution of operations that are likely to fail.
    """
    def __init__(self, name: str, config: CircuitBreakerConfig, event_bus: EventBus | None = None):
        self.name = name
        self.config = config
        self._event_bus = event_bus
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = 0.0

    @property
    def state(self) -> CircuitState:
        return self._state

    def _open_circuit(self, reason: str) -> None:
        self._state = CircuitState.OPEN
        self._last_failure_time = time.time()
        logger.warning(f"Circuit '{self.name}' opened. Reason: {reason}")
        if self._event_bus:
            self._event_bus.publish(CircuitOpenedEvent(circuit_name=self.name, reason=reason))

    def _close_circuit(self) -> None:
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        logger.info(f"Circuit '{self.name}' closed.")
        if self._event_bus:
            self._event_bus.publish(CircuitClosedEvent(circuit_name=self.name))

    def _half_open_circuit(self) -> None:
        self._state = CircuitState.HALF_OPEN
        logger.info(f"Circuit '{self.name}' transitioning to HALF-OPEN.")

    def _check_state_transition(self) -> None:
        if self._state == CircuitState.OPEN:
            time_since_failure = time.time() - self._last_failure_time
            if time_since_failure >= self.config.recovery_timeout_seconds:
                self._half_open_circuit()

    def call(self, operation: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Executes the operation if the circuit is closed or half-open."""
        self._check_state_transition()

        if self._state == CircuitState.OPEN:
            raise CircuitBreakerOpenError(f"Circuit '{self.name}' is OPEN.")

        try:
            result = operation(*args, **kwargs)
            if self._state == CircuitState.HALF_OPEN:
                self._close_circuit()
            return result
        except Exception as e:
            self._failure_count += 1
            if self._state == CircuitState.HALF_OPEN or self._failure_count >= self.config.failure_threshold:
                self._open_circuit(str(e))
            raise e
