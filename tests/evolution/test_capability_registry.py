import uuid
from tradiba.evolution.models.capability import Capability, CapabilityStatus
from tradiba.evolution.capability_registry import CapabilityRegistry

def test_capability_registry():
    registry = CapabilityRegistry()
    cap_id = uuid.uuid4()
    cap = Capability(
        id=cap_id,
        name="test_plugin",
        version="1.0.0",
        status=CapabilityStatus.SUPPORTED,
        owner="test",
        dependencies=[]
    )
    
    registry.register(cap)
    
    retrieved = registry.get(cap_id)
    assert retrieved is not None
    assert retrieved.name == "test_plugin"
    
    all_caps = registry.list_all()
    assert len(all_caps) == 1
