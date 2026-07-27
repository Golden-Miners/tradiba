from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any

class NotificationSeverity(str, Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class DeliveryStatus(str, Enum):
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"
    READ = "read"

class Notification(BaseModel):
    id: str
    type: str
    severity: NotificationSeverity
    recipient_id: str
    title: str
    message: str
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: DeliveryStatus = DeliveryStatus.PENDING
    channels_attempted: list[str] = Field(default_factory=list)
