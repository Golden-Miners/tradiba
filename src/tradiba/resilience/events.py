from dataclasses import dataclass
from uuid import UUID
from tradiba.events.event import DomainEvent

@dataclass(frozen=True)
class CheckpointCreatedEvent(DomainEvent):
    checkpoint_id: UUID
    portfolio_version: int
    event_sequence: int

@dataclass(frozen=True)
class RecoveryCompletedEvent(DomainEvent):
    checkpoint_id: UUID
    restored_event_sequence: int

@dataclass(frozen=True)
class CircuitOpenedEvent(DomainEvent):
    circuit_name: str
    reason: str

@dataclass(frozen=True)
class CircuitClosedEvent(DomainEvent):
    circuit_name: str

@dataclass(frozen=True)
class FailoverActivatedEvent(DomainEvent):
    component_name: str
    secondary_target: str

@dataclass(frozen=True)
class ReconciliationCompletedEvent(DomainEvent):
    discrepancies_found: int
    details: dict[str, int]
