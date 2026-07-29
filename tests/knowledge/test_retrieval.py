from tradiba.knowledge.retrieval.semantic_search import SemanticSearch

def test_retrieval():
    search = SemanticSearch()
    res = search.search("show me incident 123")
    assert len(res) == 1
    assert res[0]["type"] == "incident"
