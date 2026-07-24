from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from enum import Enum

class PendingOrderStatus(Enum):
    PENDING = "PENDING"
    FILLED = "FILLED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

@dataclass(slots=True)
class PendingOrder:
    ticket: int
    symbol: str
    volume: Decimal
    order_type: str
    expiry: datetime | None
    broker_state: str
    status: PendingOrderStatus
