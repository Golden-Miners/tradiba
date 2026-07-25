import tracemalloc
from typing import Any, TypeVar, Generic, Callable
from tradiba.performance.profiler import Profiler

T = TypeVar('T')

class MemoryProfiler(Profiler):
    """
    Profiles memory allocations and peak usage.
    """
    def __init__(self) -> None:
        self.started = False
        self._current_mb = 0.0
        self._peak_mb = 0.0
        
    def start(self) -> None:
        if not self.started:
            tracemalloc.start()
            self.started = True
            
    def stop(self) -> None:
        if self.started:
            current, peak = tracemalloc.get_traced_memory()
            self._current_mb = current / 1024 / 1024
            self._peak_mb = peak / 1024 / 1024
            tracemalloc.stop()
            self.started = False
            
    def get_results(self) -> dict[str, Any]:
        if self.started:
            current, peak = tracemalloc.get_traced_memory()
            return {
                "current_mb": current / 1024 / 1024,
                "peak_mb": peak / 1024 / 1024
            }
        return {
            "current_mb": self._current_mb,
            "peak_mb": self._peak_mb
        }

class MemoryPool(Generic[T]):
    """
    Reuses objects to prevent excessive allocations during hot loops.
    """
    def __init__(self, factory: Callable[..., T]) -> None:
        self._factory = factory
        self._pool: list[T] = []
        
    def acquire(self) -> T:
        if self._pool:
            return self._pool.pop()
        return self._factory()
        
    def release(self, obj: T) -> None:
        # User is responsible for clearing the object state before release
        self._pool.append(obj)
