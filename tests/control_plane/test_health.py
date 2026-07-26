import uuid
from tradiba.control_plane.health import GlobalHealthDashboard
from tradiba.control_plane.registry import FleetRegistry
from tradiba.control_plane.cluster import Cluster, Environment, ClusterStatus

def test_global_health_summary():
    registry = FleetRegistry()
    
    registry.register_cluster(Cluster(uuid.uuid4(), "c1", Environment.DEVELOPMENT, "r1", "v1", ClusterStatus.ONLINE))
    registry.register_cluster(Cluster(uuid.uuid4(), "c2", Environment.STAGING, "r1", "v1", ClusterStatus.DEGRADED))
    registry.register_cluster(Cluster(uuid.uuid4(), "c3", Environment.PRODUCTION, "r1", "v1", ClusterStatus.OFFLINE))
    
    dashboard = GlobalHealthDashboard(registry)
    summary = dashboard.generate_summary()
    
    assert summary.total_clusters == 3
    assert summary.online == 1
    assert summary.degraded == 1
    assert summary.offline == 1
    assert summary.upgrading == 0
