import concurrent.futures
from typing import Callable, Any

class Bulkhead:
    """
    Isolates failures by running operations in separate execution pools.
    """
    def __init__(self, name: str, max_workers: int = 10):
        self.name = name
        self._executor = concurrent.futures.ThreadPoolExecutor(
            max_workers=max_workers,
            thread_name_prefix=f"Bulkhead-{name}"
        )

    def execute(self, operation: Callable[..., Any], *args: Any, **kwargs: Any) -> concurrent.futures.Future[Any]:
        """Submits the operation to the isolated thread pool."""
        return self._executor.submit(operation, *args, **kwargs)

    def shutdown(self) -> None:
        self._executor.shutdown(wait=True)
