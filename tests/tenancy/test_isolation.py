import uuid
import pytest
from tradiba.tenancy.isolation import IsolationEnforcer
from tradiba.tenancy.context import TenantContextManager
from tradiba.tenancy.exceptions import TenantIsolationError

def test_isolation_enforcement():
    enforcer = IsolationEnforcer()
    t1 = uuid.uuid4()
    t2 = uuid.uuid4()
    
    TenantContextManager.set_tenant_id(t1)
    
    # Should not raise
    enforcer.validate_access(t1)
    
    # Should raise
    with pytest.raises(TenantIsolationError):
        enforcer.validate_access(t2)
        
    TenantContextManager.clear()
