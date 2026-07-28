from typing import Dict

class FleetManager:
    """
    Fleet health scoring, rolling upgrades, and regional failover management.
    """
    def __init__(self):
        self.nodes: Dict[str, str] = {}

    def register_node(self, node_id: str) -> None:
        self.nodes[node_id] = "healthy"

    def failover(self, node_id: str) -> bool:
        if node_id in self.nodes:
            self.nodes[node_id] = "failed_over"
            return True
        return False
