from dataclasses import dataclass
from uuid import UUID
from tradiba.events.event import DomainEvent
from tradiba.tenancy.models.tenant import TenantTier

@dataclass(frozen=True)
class TenantCreatedEvent(DomainEvent):
    tenant_id: UUID
    name: str
    tier: TenantTier

@dataclass(frozen=True)
class TenantActivatedEvent(DomainEvent):
    tenant_id: UUID

@dataclass(frozen=True)
class TenantSuspendedEvent(DomainEvent):
    tenant_id: UUID

@dataclass(frozen=True)
class QuotaExceededEvent(DomainEvent):
    tenant_id: UUID
    resource: str

@dataclass(frozen=True)
class WorkspaceProvisionedEvent(DomainEvent):
    tenant_id: UUID

@dataclass(frozen=True)
class UsageRecordedEvent(DomainEvent):
    tenant_id: UUID
    resource: str
    units: float
