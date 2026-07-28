from tradiba.hermes.federation.resilience.mesh_healer import MeshHealer

def test_resilience():
    mh = MeshHealer()
    mh.handle_partition("node2")
    assert "node2" in mh.partitions
    
    res = mh.resolve_conflict({"timestamp": 1}, {"timestamp": 2})
    assert res["timestamp"] == 2
