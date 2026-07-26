from typing import Dict
from uuid import UUID
from tradiba.tenancy.models.tenant import Tenant

class TenantRegistry:
    """Mock persistence layer storing registered Tenants."""
    
    def __init__(self) -> None:
        self._store: Dict[UUID, Tenant] = {}
        
    def save(self, tenant: Tenant) -> None:
        self._store[tenant.tenant_id] = tenant
        
    def get(self, tenant_id: UUID) -> Tenant | None:
        return self._store.get(tenant_id)
