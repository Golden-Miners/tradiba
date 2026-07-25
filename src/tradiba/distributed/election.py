import asyncio
import logging
from typing import Optional

from tradiba.distributed.coordination.lease import Lease

logger = logging.getLogger(__name__)

class LeaderElection:
    """
    Manages leader election for specific roles (e.g. scheduler).
    Ensures that only one node holds the lease for a resource at a time.
    """
    def __init__(self, node_id: str, resource: str, ttl_seconds: int = 15):
        self.node_id = node_id
        self.resource = resource
        self.ttl_seconds = ttl_seconds
        self.lease = Lease(owner_id=node_id, resource=resource, ttl_seconds=ttl_seconds)
        self._renew_task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Starts the election process by trying to acquire the lease."""
        acquired = await self.lease.acquire()
        if acquired:
            logger.info(f"Node {self.node_id} became leader for {self.resource}")
            self._renew_task = asyncio.create_task(self._renew_loop())

    async def stop(self) -> None:
        """Stops the election process and releases leadership if held."""
        if self._renew_task:
            self._renew_task.cancel()
            try:
                await self._renew_task
            except asyncio.CancelledError:
                pass
        await self.lease.release()
        logger.info(f"Node {self.node_id} released leadership for {self.resource}")

    @property
    def is_leader(self) -> bool:
        """Returns True if this node is currently the leader."""
        return self.lease.is_active

    async def _renew_loop(self) -> None:
        """Background task to periodically renew the lease."""
        renew_interval = max(1, self.ttl_seconds // 3)
        while True:
            await asyncio.sleep(renew_interval)
            success = await self.lease.renew()
            if not success:
                logger.error(f"Node {self.node_id} failed to renew lease for {self.resource}")
                # We lost the lease. Stop acting as leader.
                break
