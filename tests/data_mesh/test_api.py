from tradiba.data_mesh.api.endpoints import DataMeshEndpoints

def test_api():
    api = DataMeshEndpoints()
    assert api.handle_request({})["status"] == "success"
