from tradiba.distributed.cluster import ClusterRegistry

def test_cluster_registration():
    registry = ClusterRegistry()
    node_id = "node-1"
    
    registry.register(node_id, {"roles": ["api", "worker"]})
    
    assert node_id in registry.active_nodes()
    
    status = registry.node_status(node_id)
    assert status["roles"] == ["api", "worker"]
    assert "last_seen" in status
    
    registry.unregister(node_id)
    assert node_id not in registry.active_nodes()
