from tradiba.alternative_data.api.endpoints import AlternativeDataEndpoints

def test_api():
    api = AlternativeDataEndpoints()
    assert api.handle_ingest({})["status"] == "success"
