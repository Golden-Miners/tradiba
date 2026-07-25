from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

@dataclass(frozen=True)
class NodeJoinedEvent:
    node_id: str
    timestamp: datetime
    roles: list[str]

@dataclass(frozen=True)
class NodeFailedEvent:
    node_id: str
    timestamp: datetime
    reason: str

@dataclass(frozen=True)
class JobStatusChangedEvent:
    job_id: UUID
    old_status: str
    new_status: str
    timestamp: datetime
