from uuid import UUID
from typing import Dict
from tradiba.tenancy.context import TenantContextManager
from tradiba.tenancy.exceptions import QuotaExceededError

class QuotaManager:
    """Enforces resource limits for tenants."""
    
    def __init__(self) -> None:
        self._usage: Dict[UUID, Dict[str, int]] = {}
        self._limits: Dict[UUID, Dict[str, int]] = {}
        
    def set_limit(self, tenant_id: UUID, resource: str, limit: int) -> None:
        if tenant_id not in self._limits:
            self._limits[tenant_id] = {}
        self._limits[tenant_id][resource] = limit
        
    def check_and_consume(self, resource: str, amount: int = 1) -> None:
        tenant_id = TenantContextManager.get_tenant_id()
        if not tenant_id:
            return  # Default open if no tenant context
            
        limit = self._limits.get(tenant_id, {}).get(resource, float("inf"))
        current = self._usage.get(tenant_id, {}).get(resource, 0)
        
        if current + amount > limit:
            raise QuotaExceededError(f"Tenant {tenant_id} exceeded quota for {resource}")
            
        if tenant_id not in self._usage:
            self._usage[tenant_id] = {}
        self._usage[tenant_id][resource] = current + amount
