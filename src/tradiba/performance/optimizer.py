import asyncio
from typing import Callable, Any, Coroutine

class AsyncPipelineOptimizer:
    """
    Utilities for converting blocking tasks into asynchronous operations where beneficial.
    """
    @staticmethod
    async def run_in_executor(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
        """Runs a blocking synchronous function in a thread pool executor."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

    @staticmethod
    async def gather_concurrently(*coros: Coroutine[Any, Any, Any]) -> tuple[Any, ...]:
        """Awaits multiple coroutines concurrently."""
        results = await asyncio.gather(*coros)
        return tuple(results)

class SerializationOptimizer:
    """
    Provides optimized serialization routines. In a full implementation, 
    this would use msgpack or protobuf over standard json.
    """
    @staticmethod
    def optimize_dict(data: dict[str, Any]) -> dict[str, Any]:
        """Removes nulls or compresses data structure keys."""
        return {k: v for k, v in data.items() if v is not None}
