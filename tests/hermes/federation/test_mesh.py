from tradiba.hermes.federation.mesh.cognitive_mesh import CognitiveMesh

def test_mesh():
    mesh = CognitiveMesh()
    assert mesh.join("url1", "id1")
    assert "id1" in mesh.get_topology()["peers"]
    assert mesh.leave("id1")
