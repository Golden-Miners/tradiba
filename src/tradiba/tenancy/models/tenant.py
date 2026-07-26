from dataclasses import dataclass
from uuid import UUID
from enum import Enum
from datetime import datetime

class TenantTier(Enum):
    ENTERPRISE = "ENTERPRISE"
    PRO = "PRO"
    STARTER = "STARTER"

class TenantStatus(Enum):
    PROVISIONING = "PROVISIONING"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    ARCHIVED = "ARCHIVED"
    DELETED = "DELETED"

@dataclass(frozen=True)
class Tenant:
    tenant_id: UUID
    name: str
    tier: TenantTier
    status: TenantStatus
    created_at: datetime
