import uuid
import pytest
from tradiba.tenancy.quotas import QuotaManager
from tradiba.tenancy.context import TenantContextManager
from tradiba.tenancy.exceptions import QuotaExceededError

def test_quota_manager():
    manager = QuotaManager()
    t1 = uuid.uuid4()
    
    manager.set_limit(t1, "api_calls", 2)
    
    TenantContextManager.set_tenant_id(t1)
    
    manager.check_and_consume("api_calls", 1)
    manager.check_and_consume("api_calls", 1)
    
    with pytest.raises(QuotaExceededError):
        manager.check_and_consume("api_calls", 1)
        
    TenantContextManager.clear()
