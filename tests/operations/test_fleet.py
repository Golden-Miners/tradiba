from tradiba.operations.fleet.manager import FleetManager

def test_fleet():
    manager = FleetManager()
    manager.register_node("n1")
    assert manager.nodes["n1"] == "healthy"
    assert manager.failover("n1")
    assert not manager.failover("n2")
