from dataclasses import dataclass
from tradiba.events.event import DomainEvent
from uuid import UUID

@dataclass(frozen=True)
class HypothesisCreatedEvent(DomainEvent):
    hypothesis_id: UUID

@dataclass(frozen=True)
class ExperimentStartedEvent(DomainEvent):
    experiment_id: UUID
    candidate_id: UUID

@dataclass(frozen=True)
class ExperimentCompletedEvent(DomainEvent):
    experiment_id: UUID
    success: bool

@dataclass(frozen=True)
class FeatureDiscoveredEvent(DomainEvent):
    feature_name: str

@dataclass(frozen=True)
class PromotionRecommendedEvent(DomainEvent):
    candidate_id: str
    target_stage: str

@dataclass(frozen=True)
class ResearchValidationCompletedEvent(DomainEvent):
    candidate_id: str
    passed: bool
