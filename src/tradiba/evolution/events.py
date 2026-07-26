from dataclasses import dataclass
from uuid import UUID
from tradiba.events.event import DomainEvent

@dataclass(frozen=True)
class CapabilityRegisteredEvent(DomainEvent):
    capability_id: UUID
    name: str
    capability_version: str

@dataclass(frozen=True)
class FeatureFlagChangedEvent(DomainEvent):
    flag_name: str
    enabled: bool

@dataclass(frozen=True)
class SchemaMigratedEvent(DomainEvent):
    schema_name: str
    new_version: str

@dataclass(frozen=True)
class MigrationCompletedEvent(DomainEvent):
    migration_id: str

@dataclass(frozen=True)
class UpgradeStartedEvent(DomainEvent):
    service: str
    target_version: str

@dataclass(frozen=True)
class UpgradeCompletedEvent(DomainEvent):
    service: str
    upgraded_version: str

@dataclass(frozen=True)
class RollbackTriggeredEvent(DomainEvent):
    service: str
    reason: str

@dataclass(frozen=True)
class CapabilityDeprecatedEvent(DomainEvent):
    capability_id: UUID
    notice: str
