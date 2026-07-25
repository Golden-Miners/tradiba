from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4

from dataclasses import field

@dataclass(slots=True, frozen=True, kw_only=True)
class DomainEvent:
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=datetime.utcnow)
    version: int = 1

    @classmethod
    def create(cls, **kwargs):
        return cls(
            event_id=uuid4(),
            occurred_at=datetime.utcnow(),
            **kwargs,
        )

    @property
    def timestamp(self) -> datetime:
        return self.occurred_at
