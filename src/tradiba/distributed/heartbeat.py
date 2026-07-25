import asyncio
import logging
from datetime import datetime
from typing import Optional

from tradiba.distributed.messaging.base import MessageBus
from tradiba.distributed.configuration import DistributedConfig
from tradiba.distributed.cluster import ClusterRegistry

logger = logging.getLogger(__name__)

class HeartbeatMonitor:
    """
    Publishes heartbeats for the current node and monitors heartbeats from other nodes.
    """
    def __init__(self, config: DistributedConfig, bus: MessageBus, registry: ClusterRegistry):
        self.config = config
        self.bus = bus
        self.registry = registry
        self._task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Start the heartbeat loop."""
        self._task = asyncio.create_task(self._run_heartbeat())
        
        # Subscribe to heartbeats from other nodes
        self.bus.subscribe("cluster.heartbeat", self._on_heartbeat)
        logger.info("Heartbeat monitor started")

    async def stop(self) -> None:
        """Stop the heartbeat loop."""
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Heartbeat monitor stopped")

    async def _run_heartbeat(self) -> None:
        while True:
            try:
                payload = {
                    "node_id": self.config.node_id,
                    "timestamp": datetime.now(),
                    "cpu_usage": 0.0, # Placeholder for real metrics
                    "memory_usage": 0.0,
                    "queue_depth": 0
                }
                self.bus.publish("cluster.heartbeat", payload)
            except Exception as e:
                logger.error(f"Failed to publish heartbeat: {e}")
            await asyncio.sleep(self.config.heartbeat_interval_seconds)

    def _on_heartbeat(self, event: dict) -> None:
        node_id = event.get("node_id")
        if node_id and node_id != self.config.node_id:
            # Update the registry with the latest heartbeat info
            self.registry.register(node_id, event)
