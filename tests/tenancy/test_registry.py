import uuid
from datetime import datetime
from tradiba.tenancy.models.tenant import Tenant, TenantTier, TenantStatus
from tradiba.tenancy.registry import TenantRegistry

def test_tenant_registry():
    registry = TenantRegistry()
    t_id = uuid.uuid4()
    t = Tenant(
        tenant_id=t_id,
        name="Test",
        tier=TenantTier.STARTER,
        status=TenantStatus.ACTIVE,
        created_at=datetime.utcnow()
    )
    
    registry.save(t)
    retrieved = registry.get(t_id)
    
    assert retrieved is not None
    assert retrieved.name == "Test"
