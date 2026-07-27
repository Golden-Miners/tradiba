from tradiba.hermes.platform.mesh.cognitive_mesh import CognitiveMesh

def test_mesh():
    mesh = CognitiveMesh()
    mesh.register_node("n1", ["trade", "research"])
    assert mesh.route_request("trade") == "n1"
    assert mesh.route_request("unknown") == ""
