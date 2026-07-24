from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum

class ExecutionStatus(Enum):
    PENDING = "PENDING"
    SUBMITTED = "SUBMITTED"
    FILLED = "FILLED"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"

@dataclass(slots=True, frozen=True)
class ExecutionReport:
    execution_id: str
    trade_plan_id: str
    broker_order_id: int | None
    symbol: str
    status: ExecutionStatus
    requested_price: Decimal
    executed_price: Decimal | None
    volume: Decimal
    submitted_at: datetime
    completed_at: datetime | None
    reason: str | None = None
