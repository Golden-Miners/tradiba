from tradiba.data_mesh.mesh.federation import DataMeshFederation

def test_mesh():
    fed = DataMeshFederation()
    assert fed.query("p1")["status"] == "ok"
