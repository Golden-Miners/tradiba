from dataclasses import dataclass
from tradiba.events.event import DomainEvent
from uuid import UUID

@dataclass(frozen=True)
class TwinSynchronizedEvent(DomainEvent):
    twin_id: UUID
    source_cluster: UUID
    state_version: int

@dataclass(frozen=True)
class DriftDetectedEvent(DomainEvent):
    twin_id: UUID
    drift_type: str
    severity: str

@dataclass(frozen=True)
class DeploymentValidatedEvent(DomainEvent):
    candidate_version: str
    passed: bool

@dataclass(frozen=True)
class ScenarioCompletedEvent(DomainEvent):
    scenario_name: str
    projected_pnl: float

@dataclass(frozen=True)
class ShadowExecutionCompletedEvent(DomainEvent):
    twin_id: UUID
    simulated_fills: int
