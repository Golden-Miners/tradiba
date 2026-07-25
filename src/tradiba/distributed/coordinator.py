import logging
from tradiba.distributed.configuration import DistributedConfig
from tradiba.distributed.heartbeat import HeartbeatMonitor
from tradiba.distributed.scheduler import DistributedScheduler

logger = logging.getLogger(__name__)

class NodeCoordinator:
    """
    Coordinates the lifecycle of all distributed components on a node.
    """
    def __init__(
        self,
        config: DistributedConfig,
        heartbeat_monitor: HeartbeatMonitor,
        scheduler: DistributedScheduler,
    ):
        self.config = config
        self.heartbeat_monitor = heartbeat_monitor
        self.scheduler = scheduler

    async def start(self) -> None:
        """Start all distributed coordination tasks for this node."""
        logger.info(f"Starting NodeCoordinator on {self.config.node_id}")
        await self.heartbeat_monitor.start()
        await self.scheduler.start()

    async def stop(self) -> None:
        """Stop all distributed coordination tasks."""
        logger.info(f"Stopping NodeCoordinator on {self.config.node_id}")
        await self.scheduler.stop()
        await self.heartbeat_monitor.stop()
