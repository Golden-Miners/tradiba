from typing import Dict, Any, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ClusterRegistry:
    """
    Maintains metadata for all nodes in the cluster.
    Supports routing, diagnostics, and scaling decisions.
    """
    def __init__(self):
        self._nodes: Dict[str, dict[str, Any]] = {}

    def register(self, node_id: str, metadata: dict[str, Any]) -> None:
        """Register a node with the cluster."""
        metadata['last_seen'] = datetime.now()
        self._nodes[node_id] = metadata
        logger.info(f"Node '{node_id}' registered in cluster")

    def unregister(self, node_id: str) -> None:
        """Unregister a node."""
        if node_id in self._nodes:
            del self._nodes[node_id]
            logger.info(f"Node '{node_id}' unregistered")

    def active_nodes(self) -> List[str]:
        """List active node IDs."""
        return list(self._nodes.keys())

    def node_status(self, node_id: str) -> dict[str, Any]:
        """Get status of a specific node."""
        return self._nodes.get(node_id, {})
