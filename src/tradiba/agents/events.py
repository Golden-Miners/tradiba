from dataclasses import dataclass
from tradiba.events.event import DomainEvent

@dataclass(frozen=True)
class AgentStartedEvent(DomainEvent):
    agent_name: str
    context_id: str

@dataclass(frozen=True)
class RecommendationCreatedEvent(DomainEvent):
    recommendation_id: str
    agent_name: str

@dataclass(frozen=True)
class RecommendationApprovedEvent(DomainEvent):
    recommendation_id: str
    approver: str

@dataclass(frozen=True)
class KnowledgeUpdatedEvent(DomainEvent):
    source: str
    relation: str
    target: str
