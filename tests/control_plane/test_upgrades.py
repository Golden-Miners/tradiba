import uuid
from tradiba.control_plane.upgrades import RollingUpgradeCoordinator
from tradiba.control_plane.cluster import Cluster, Environment, ClusterStatus

def test_rolling_upgrade_success():
    coordinator = RollingUpgradeCoordinator()
    
    clusters = [
        Cluster(uuid.uuid4(), "dev1", Environment.DEVELOPMENT, "us-east", "v1", ClusterStatus.ONLINE),
        Cluster(uuid.uuid4(), "prod1", Environment.PRODUCTION, "us-east", "v1", ClusterStatus.ONLINE)
    ]
    
    assert coordinator.execute_upgrade("v2", clusters) is True
    assert clusters[0].version == "v2"
    assert clusters[1].version == "v2"
    
def test_rolling_upgrade_failure():
    coordinator = RollingUpgradeCoordinator()
    
    clusters = [
        Cluster(uuid.uuid4(), "dev1", Environment.DEVELOPMENT, "us-east", "v1", ClusterStatus.DEGRADED),
        Cluster(uuid.uuid4(), "prod1", Environment.PRODUCTION, "us-east", "v1", ClusterStatus.ONLINE)
    ]
    
    # Fails at dev stage due to degraded status
    assert coordinator.execute_upgrade("v2", clusters) is False
    assert clusters[1].version == "v1" # Prod should not have upgraded
