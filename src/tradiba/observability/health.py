from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List


@dataclass(slots=True)
class HealthStatus:
    name: str
    healthy: bool
    message: str = ""


class HealthCheck(ABC):
    """Interface for component health checks."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def check(self) -> HealthStatus:
        pass


class HealthManager:
    """Manages liveness and readiness checks."""
    
    def __init__(self):
        self._checks: List[HealthCheck] = []
        self._liveness: bool = True

    def register(self, check: HealthCheck) -> None:
        self._checks.append(check)

    def is_alive(self) -> bool:
        """Liveness check: process is running and not deadlocked."""
        return self._liveness
        
    def set_liveness(self, alive: bool) -> None:
        self._liveness = alive

    def is_ready(self) -> bool:
        """Readiness check: dependencies are accessible."""
        return all(c.check().healthy for c in self._checks)

    def get_status(self) -> Dict[str, dict]:
        """Returns detailed status of all dependencies."""
        status = {}
        for c in self._checks:
            result = c.check()
            status[result.name] = {
                "healthy": result.healthy,
                "message": result.message
            }
        return status
