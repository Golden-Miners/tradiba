import uuid
from tradiba.data_platform.retention import RetentionManager

def test_retention_manager():
    manager = RetentionManager()
    ds_id = uuid.uuid4()
    
    # tick_data limit is 5 years = 1825 days
    assert manager.evaluate(ds_id, "tick_data", 1000) is False
    assert manager.evaluate(ds_id, "tick_data", 2000) is True
    
    # research limit is 90 days
    assert manager.evaluate(ds_id, "research", 80) is False
    assert manager.evaluate(ds_id, "research", 91) is True
    
    manager.purge(ds_id)
    assert ds_id in manager._purged
