from dataclasses import dataclass
from typing import Optional
from tradiba.events.event import DomainEvent

@dataclass(slots=True, frozen=True)
class EventEnvelope:
    aggregate_id: str
    aggregate_type: str
    sequence: int
    event: DomainEvent
    correlation_id: Optional[str] = None
    causation_id: Optional[str] = None
