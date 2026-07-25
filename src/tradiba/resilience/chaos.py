import logging
import random
import time
from typing import Callable, Any
from tradiba.resilience.exceptions import ChaosInjectedError

logger = logging.getLogger(__name__)

class ChaosExperiment:
    """
    Framework for injecting controlled faults into the system.
    WARNING: Never run in production without explicit authorization.
    """
    def __init__(self, name: str, enabled: bool = False):
        self.name = name
        self.enabled = enabled

    def run(self, operation: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """
        Executes the operation, potentially injecting a fault.
        """
        if not self.enabled:
            return operation(*args, **kwargs)

        fault_type = self._determine_fault()
        
        if fault_type == "latency":
            self._inject_latency()
        elif fault_type == "exception":
            self._inject_exception()
            
        return operation(*args, **kwargs)

    def _determine_fault(self) -> str | None:
        """Randomly selects a fault type to inject based on probability."""
        roll = random.random()
        if roll < 0.05:
            return "exception"
        elif roll < 0.15:
            return "latency"
        return None

    def _inject_latency(self) -> None:
        delay = random.uniform(1.0, 5.0)
        logger.warning(f"ChaosExperiment '{self.name}': Injecting {delay:.2f}s latency.")
        time.sleep(delay)

    def _inject_exception(self) -> None:
        logger.error(f"ChaosExperiment '{self.name}': Injecting ChaosInjectedError.")
        raise ChaosInjectedError(f"Simulated failure by ChaosExperiment '{self.name}'.")
