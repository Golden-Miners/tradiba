from tradiba.knowledge.api.endpoints import KnowledgeEndpoints

def test_api():
    api = KnowledgeEndpoints()
    assert api.handle_ingest({})["status"] == "ingested"
    assert "results" in api.handle_search("test")
