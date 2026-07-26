import uuid
from tradiba.data_platform.query import AnalyticsQueryEngine
from tradiba.data_platform.lakehouse import DataLakehouse, StorageZone

def test_query_engine():
    lakehouse = DataLakehouse()
    engine = AnalyticsQueryEngine(lakehouse)
    
    ds_id = uuid.uuid4()
    lakehouse.write_to_zone(StorageZone.CURATED, ds_id, [])
    
    res = engine.execute({"dataset_id": ds_id})
    assert len(res) == 1
    assert res[0]["dataset_id"] == str(ds_id)
    assert res[0]["zone"] == StorageZone.CURATED.value
    
    res_empty = engine.execute({"dataset_id": uuid.uuid4()})
    assert len(res_empty) == 0
