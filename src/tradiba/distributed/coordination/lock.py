import logging
from typing import Optional
from contextlib import asynccontextmanager

from tradiba.distributed.exceptions import LockAcquisitionError

logger = logging.getLogger(__name__)

class DistributedLock:
    """
    Distributed Lock for singleton operations like DB migrations,
    snapshot creation, etc. Avoid long-lived locks.
    """
    def __init__(self, name: str, node_id: str, ttl_seconds: int = 10):
        self.name = name
        self.node_id = node_id
        self.ttl_seconds = ttl_seconds
        self._acquired = False

    async def acquire(self, timeout_seconds: Optional[int] = None) -> bool:
        """Attempt to acquire the lock."""
        # Placeholder for real distributed lock acquisition
        logger.debug(f"Node {self.node_id} acquired lock {self.name}")
        self._acquired = True
        return True

    async def release(self) -> None:
        """Release the lock."""
        if self._acquired:
            logger.debug(f"Node {self.node_id} released lock {self.name}")
            self._acquired = False

    @asynccontextmanager
    async def __call__(self, timeout_seconds: Optional[int] = None):
        """Context manager support."""
        acquired = await self.acquire(timeout_seconds)
        if not acquired:
            raise LockAcquisitionError(f"Could not acquire lock '{self.name}' within {timeout_seconds}s")
        try:
            yield self
        finally:
            await self.release()
