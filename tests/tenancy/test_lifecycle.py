import uuid
from datetime import datetime
from tradiba.tenancy.lifecycle import TenantLifecycle
from tradiba.tenancy.registry import TenantRegistry
from tradiba.tenancy.models.tenant import Tenant, TenantTier, TenantStatus

def test_tenant_lifecycle():
    registry = TenantRegistry()
    lifecycle = TenantLifecycle(registry)
    
    t_id = uuid.uuid4()
    t = Tenant(
        tenant_id=t_id,
        name="Test",
        tier=TenantTier.STARTER,
        status=TenantStatus.PROVISIONING,
        created_at=datetime.utcnow()
    )
    registry.save(t)
    
    updated = lifecycle.activate(t_id)
    assert updated.status == TenantStatus.ACTIVE
    
    suspended = lifecycle.suspend(t_id)
    assert suspended.status == TenantStatus.SUSPENDED
