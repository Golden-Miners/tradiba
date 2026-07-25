from uuid import uuid4
from datetime import datetime
from tradiba.research.datasets import Dataset, DatasetRegistry

def test_dataset_registration():
    registry = DatasetRegistry()
    ds_id = uuid4()
    
    ds = Dataset(
        dataset_id=ds_id,
        symbol="BTCUSD",
        timeframe="1h",
        start=datetime(2025, 1, 1),
        end=datetime(2025, 1, 31),
        feature_version="v1",
        label_version="v1"
    )
    
    registry.register(ds)
    retrieved = registry.get(ds_id)
    
    assert retrieved is not None
    assert retrieved.symbol == "BTCUSD"
    assert retrieved.feature_version == "v1"
