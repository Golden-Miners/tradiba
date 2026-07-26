from uuid import UUID
from tradiba.tenancy.context import TenantContextManager
from tradiba.tenancy.exceptions import TenantIsolationError

DEFAULT_TENANT_ID = UUID(int=0)

class IsolationEnforcer:
    """Validates that requested resources belong to the current context."""
    
    def __init__(self, fallback_to_default: bool = True):
        self.fallback_to_default = fallback_to_default

    def validate_access(self, resource_tenant_id: UUID) -> None:
        """
        Validates if the current context has access to the resource.
        """
        current_tenant = TenantContextManager.get_tenant_id()
        
        # Backward compatibility for single-tenant platforms without explicit context
        if current_tenant is None and self.fallback_to_default:
            current_tenant = DEFAULT_TENANT_ID

        if current_tenant != resource_tenant_id:
            raise TenantIsolationError(
                f"Context tenant {current_tenant} cannot access resource of tenant {resource_tenant_id}"
            )
