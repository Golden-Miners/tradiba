from tradiba.modelops.api.endpoints import ModelOpsEndpoints

def test_api():
    api = ModelOpsEndpoints()
    assert api.handle_train({})["status"] == "success"
