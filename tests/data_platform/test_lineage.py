import uuid
import pytest
from tradiba.data_platform.lineage import LineageTracker
from tradiba.data_platform.exceptions import LineageError

def test_lineage_tracking():
    tracker = LineageTracker()
    
    parent1 = uuid.uuid4()
    parent2 = uuid.uuid4()
    child = uuid.uuid4()
    
    tracker.record_derivation(child, [parent1, parent2])
    
    parents = tracker.get_parents(child)
    assert len(parents) == 2
    assert parent1 in parents
    assert parent2 in parents
    
def test_lineage_empty_parents():
    tracker = LineageTracker()
    child = uuid.uuid4()
    
    with pytest.raises(LineageError):
        tracker.record_derivation(child, [])
