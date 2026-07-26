class TenantIsolationError(Exception):
    """Raised when cross-tenant data access is attempted."""
    pass

class QuotaExceededError(Exception):
    """Raised when a tenant exceeds their resource quota."""
    pass

class TenantNotFoundError(Exception):
    """Raised when a tenant cannot be found in the registry."""
    pass
