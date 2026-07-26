import uuid
from tradiba.data_platform.catalog import DataCatalog, Dataset

def test_catalog_registration():
    catalog = DataCatalog()
    
    ds_id = uuid.uuid4()
    ds = Dataset(
        dataset_id=ds_id,
        name="tick_data_aapl",
        owner="data_engineering",
        schema_version="v1",
        retention_policy="tick_data",
        classification="market_data"
    )
    
    catalog.register(ds)
    
    retrieved = catalog.get_dataset(ds_id)
    assert retrieved is not None
    assert retrieved.name == "tick_data_aapl"
    assert len(catalog.list_datasets()) == 1
