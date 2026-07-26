import uuid
from tradiba.tenancy.events import TenantCreatedEvent
from tradiba.tenancy.models.tenant import TenantTier

def test_events_creation():
    e = TenantCreatedEvent(
        tenant_id=uuid.uuid4(),
        name="Acme",
        tier=TenantTier.ENTERPRISE
    )
    assert e.name == "Acme"
