from uuid import uuid4
from tradiba.tenancy.context import TenantContextManager

def test_tenant_context():
    tenant_id = uuid4()
    
    TenantContextManager.set_tenant_id(tenant_id)
    assert TenantContextManager.get_tenant_id() == tenant_id
    
    TenantContextManager.clear()
    assert TenantContextManager.get_tenant_id() is None
