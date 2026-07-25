from abc import ABC, abstractmethod
from typing import Any

class Profiler(ABC):
    """
    Base trait for performance profilers.
    """
    @abstractmethod
    def start(self) -> None:
        pass
        
    @abstractmethod
    def stop(self) -> None:
        pass
        
    @abstractmethod
    def get_results(self) -> dict[str, Any]:
        pass
