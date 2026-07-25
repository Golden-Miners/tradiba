from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

class JobType(Enum):
    BACKTEST = "BACKTEST"
    OPTIMIZATION = "OPTIMIZATION"
    REPLAY = "REPLAY"
    REPORT = "REPORT"
    GENERAL = "GENERAL"

class JobStatus(Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

@dataclass
class Job:
    id: UUID
    type: JobType
    status: JobStatus
    priority: int
    payload: dict[str, Any]
    created_at: datetime
    updated_at: datetime
    error_message: Optional[str] = None
