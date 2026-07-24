from dataclasses import dataclass
from tradiba.events.base import Event
from .models import ExecutionReport

@dataclass(slots=True, frozen=True)
class OrderSubmittedEvent(Event):
    report: ExecutionReport

@dataclass(slots=True, frozen=True)
class OrderFilledEvent(Event):
    report: ExecutionReport

@dataclass(slots=True, frozen=True)
class OrderRejectedEvent(Event):
    report: ExecutionReport

@dataclass(slots=True, frozen=True)
class ExecutionFailedEvent(Event):
    report: ExecutionReport
