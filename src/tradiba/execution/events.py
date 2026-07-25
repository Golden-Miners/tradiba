from dataclasses import dataclass
from tradiba.events.event import DomainEvent
from .models import ExecutionReport

@dataclass(slots=True, frozen=True)
class OrderSubmittedEvent(DomainEvent):
    report: ExecutionReport

@dataclass(slots=True, frozen=True)
class OrderFilledEvent(DomainEvent):
    report: ExecutionReport

@dataclass(slots=True, frozen=True)
class OrderRejectedEvent(DomainEvent):
    report: ExecutionReport

@dataclass(slots=True, frozen=True)
class ExecutionFailedEvent(DomainEvent):
    report: ExecutionReport
