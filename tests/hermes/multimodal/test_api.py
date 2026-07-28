from tradiba.hermes.multimodal.api.endpoints import MultimodalEndpoints

def test_api():
    api = MultimodalEndpoints()
    assert api.handle_upload(b"data")["status"] == "uploaded"
    assert api.handle_analyze({})["analysis"] == "complete"
