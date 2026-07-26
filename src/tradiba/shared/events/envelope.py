from dataclasses import dataclass, field
from datetime import datetime
import uuid

@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events."""
    event_id: uuid.UUID = field(default_factory=uuid.uuid4)
    occurred_on: datetime = field(default_factory=datetime.utcnow)

@dataclass(frozen=True)
class EventEnvelope:
    """Standard envelope for dispatching events across bounded contexts."""
    event: DomainEvent
    source_context: str
    version: str = "1.0"
