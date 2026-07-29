from tradiba.knowledge.ingestion.pipeline import KnowledgeIngestionPipeline

def test_ingestion():
    pipeline = KnowledgeIngestionPipeline()
    res = pipeline.ingest("source", {})
    assert res["status"] == "ingested"
    assert res["source"] == "source"
