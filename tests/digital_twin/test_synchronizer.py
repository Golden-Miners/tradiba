from uuid import uuid4
from tradiba.digital_twin.synchronizer import TwinSynchronizer

def test_twin_synchronization():
    sync = TwinSynchronizer()
    cluster_id = uuid4()
    
    twin = sync.synchronize(cluster_id)
    assert twin.source_cluster == cluster_id
    assert twin.state_version == 1
    
    assert sync.validate() is True
    assert "successful" in sync.report()
