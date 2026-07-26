import uuid
from tradiba.control_plane.cluster import Cluster, Environment, ClusterStatus
from tradiba.control_plane.registry import FleetRegistry

def test_cluster_registration():
    registry = FleetRegistry()
    cluster_id = uuid.uuid4()
    
    cluster = Cluster(
        cluster_id=cluster_id,
        name="eu-west-staging",
        environment=Environment.STAGING,
        region="eu-west-1",
        version="v2.1",
        status=ClusterStatus.ONLINE
    )
    
    registry.register_cluster(cluster)
    retrieved = registry.get_cluster(cluster_id)
    
    assert retrieved is not None
    assert retrieved.name == "eu-west-staging"
    assert len(registry.list_clusters()) == 1
