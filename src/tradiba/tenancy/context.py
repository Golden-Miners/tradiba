from contextvars import ContextVar
from uuid import UUID
from typing import Optional

_tenant_context: ContextVar[Optional[UUID]] = ContextVar("tenant_context", default=None)

class TenantContextManager:
    """Manages the current tenant context for execution flow."""
    
    @staticmethod
    def set_tenant_id(tenant_id: UUID) -> None:
        _tenant_context.set(tenant_id)
        
    @staticmethod
    def get_tenant_id() -> Optional[UUID]:
        return _tenant_context.get()

    @staticmethod
    def clear() -> None:
        _tenant_context.set(None)
