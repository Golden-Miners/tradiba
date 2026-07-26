from uuid import UUID
from tradiba.control_plane.cluster import Cluster

class FleetRegistry:
    """Global inventory of managed clusters."""
    def __init__(self) -> None:
        self._clusters: dict[UUID, Cluster] = {}

    def register_cluster(self, cluster: Cluster) -> None:
        self._clusters[cluster.cluster_id] = cluster

    def get_cluster(self, cluster_id: UUID) -> Cluster | None:
        return self._clusters.get(cluster_id)
        
    def list_clusters(self) -> list[Cluster]:
        return list(self._clusters.values())
