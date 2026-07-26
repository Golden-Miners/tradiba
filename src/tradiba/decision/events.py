from dataclasses import dataclass
from uuid import UUID
from tradiba.events.event import DomainEvent

@dataclass(frozen=True)
class DecisionCreatedEvent(DomainEvent):
    decision_id: UUID

@dataclass(frozen=True)
class DecisionEvaluatedEvent(DomainEvent):
    decision_id: UUID
    passed_policy: bool

@dataclass(frozen=True)
class DecisionSimulationCompletedEvent(DomainEvent):
    decision_id: UUID
    projected_risk: str

@dataclass(frozen=True)
class DecisionApprovedEvent(DomainEvent):
    decision_id: UUID

@dataclass(frozen=True)
class DecisionRejectedEvent(DomainEvent):
    decision_id: UUID

@dataclass(frozen=True)
class DecisionExecutedEvent(DomainEvent):
    decision_id: UUID
