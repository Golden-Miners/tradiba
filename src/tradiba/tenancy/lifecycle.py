from uuid import UUID
import dataclasses
from tradiba.tenancy.models.tenant import Tenant, TenantStatus
from tradiba.tenancy.registry import TenantRegistry
from tradiba.tenancy.exceptions import TenantNotFoundError

class TenantLifecycle:
    """Handles tenant operations and state transitions."""
    
    def __init__(self, registry: TenantRegistry) -> None:
        self.registry = registry

    def activate(self, tenant_id: UUID) -> Tenant:
        tenant = self.registry.get(tenant_id)
        if not tenant:
            raise TenantNotFoundError(f"Tenant {tenant_id} not found.")
            
        updated = dataclasses.replace(tenant, status=TenantStatus.ACTIVE)
        self.registry.save(updated)
        return updated
        
    def suspend(self, tenant_id: UUID) -> Tenant:
        tenant = self.registry.get(tenant_id)
        if not tenant:
            raise TenantNotFoundError(f"Tenant {tenant_id} not found.")
            
        updated = dataclasses.replace(tenant, status=TenantStatus.SUSPENDED)
        self.registry.save(updated)
        return updated
