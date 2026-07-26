import uuid
from tradiba.evolution.event_versioning import EventVersioning, VersionedEventEnvelope

def test_event_versioning():
    versioning = EventVersioning()
    
    event = VersionedEventEnvelope(
        event_id=uuid.uuid4(),
        event_type="TradeExecuted",
        version="v1",
        tenant_id=uuid.uuid4(),
        payload={},
        metadata={}
    )
    
    upgraded = versioning.upgrade_event(event, "v2")
    assert upgraded.version == "v2"
