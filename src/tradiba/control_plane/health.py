from dataclasses import dataclass
from tradiba.control_plane.registry import FleetRegistry
from tradiba.control_plane.cluster import ClusterStatus

@dataclass
class FleetHealthSummary:
    total_clusters: int
    online: int
    offline: int
    degraded: int
    upgrading: int

class GlobalHealthDashboard:
    """Aggregates health across the entire managed fleet."""
    def __init__(self, registry: FleetRegistry) -> None:
        self.registry = registry

    def generate_summary(self) -> FleetHealthSummary:
        clusters = self.registry.list_clusters()
        
        return FleetHealthSummary(
            total_clusters=len(clusters),
            online=sum(1 for c in clusters if c.status == ClusterStatus.ONLINE),
            offline=sum(1 for c in clusters if c.status == ClusterStatus.OFFLINE),
            degraded=sum(1 for c in clusters if c.status == ClusterStatus.DEGRADED),
            upgrading=sum(1 for c in clusters if c.status == ClusterStatus.UPGRADING),
        )
