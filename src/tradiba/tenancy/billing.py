from tradiba.tenancy.context import TenantContextManager
import logging

logger = logging.getLogger(__name__)

class BillingHooks:
    """Exposes usage records for compute, storage, API calls, etc."""
    
    def record_usage(self, resource: str, units: float) -> None:
        tenant_id = TenantContextManager.get_tenant_id()
        if tenant_id:
            logger.info(f"Billing: Tenant {tenant_id} consumed {units} units of {resource}")
            # Real implementation would publish a UsageRecordedEvent
