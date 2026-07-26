from dataclasses import dataclass
from enum import Enum
from uuid import UUID
from datetime import timedelta

class TaskType(Enum):
    MANUAL = "manual"
    AUTOMATED = "automated"
    APPROVAL = "approval"
    SCHEDULED = "scheduled"
    EXTERNAL = "external"

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass(slots=True)
class WorkflowTask:
    task_id: UUID
    type: TaskType
    status: TaskStatus
    owner: str | None
    timeout: timedelta
