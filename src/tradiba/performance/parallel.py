import concurrent.futures
from typing import Callable, Iterable, Any

class ParallelExecutor:
    """
    Abstractions for process-based parallelism. Best suited for CPU-bound tasks
    like backtests or parameter optimizations.
    """
    def __init__(self, max_workers: int | None = None):
        self.max_workers = max_workers

    def map(self, func: Callable[..., Any], iterable: Iterable[Any]) -> list[Any]:
        """Maps a function over an iterable using a ProcessPoolExecutor."""
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            return list(executor.map(func, iterable))

    def submit_all(self, tasks: list[tuple[Callable[..., Any], tuple[Any, ...]]]) -> list[Any]:
        """Submits multiple heterogenous tasks."""
        with concurrent.futures.ProcessPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [executor.submit(func, *args) for func, args in tasks]
            return [future.result() for future in concurrent.futures.as_completed(futures)]
