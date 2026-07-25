from dataclasses import dataclass
from tradiba.events.event import DomainEvent
from .aggregate import Portfolio
from .position import Position
from .order import PendingOrder

@dataclass(slots=True, frozen=True)
class PortfolioUpdatedEvent(DomainEvent):
    portfolio: Portfolio

@dataclass(slots=True, frozen=True)
class PositionOpenedEvent(DomainEvent):
    position: Position

@dataclass(slots=True, frozen=True)
class PositionClosedEvent(DomainEvent):
    position: Position

@dataclass(slots=True, frozen=True)
class OrderFilledEvent(DomainEvent):
    order: PendingOrder

@dataclass(slots=True, frozen=True)
class OrderCancelledEvent(DomainEvent):
    order: PendingOrder
