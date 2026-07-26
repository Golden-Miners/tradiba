import uuid
from tradiba.data_platform.ingestion import IngestionPipeline
from tradiba.data_platform.lakehouse import DataLakehouse, StorageZone
from tradiba.data_platform.validation import DataQualityValidator

def test_ingestion_pipeline():
    lakehouse = DataLakehouse()
    validator = DataQualityValidator()
    pipeline = IngestionPipeline(lakehouse, validator)
    
    ds_id = uuid.uuid4()
    data = [{"price": 100}]
    
    assert pipeline.run(ds_id, data, {"price"}) is True
    
    assert ds_id in lakehouse.get_zone_inventory(StorageZone.RAW)
    assert ds_id in lakehouse.get_zone_inventory(StorageZone.CURATED)
