from tradiba.alternative_data.ingestion.framework import AlternativeDataIngestionFramework

def test_ingestion():
    framework = AlternativeDataIngestionFramework()
    assert framework.ingest_data("d1", {})
