from tradiba.alternative_data.documents.pipeline import DocumentPipeline

def test_documents():
    docs = DocumentPipeline()
    assert "EntityA" in docs.extract_entities("d1")
