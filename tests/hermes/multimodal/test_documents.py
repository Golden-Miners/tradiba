from tradiba.hermes.multimodal.documents.intelligence import DocumentIntelligence

def test_documents():
    di = DocumentIntelligence()
    assert "AAPL" in di.extract_entities("text")
    assert len(di.extract_tables("doc_1")) == 1
    assert di.index_document("doc_1", "content")
