from dataclasses import dataclass
from tradiba.events.base import Event
from .aggregate import Portfolio
from .position import Position
from .order import PendingOrder

@dataclass(slots=True, frozen=True)
class PortfolioUpdatedEvent(Event):
    portfolio: Portfolio

@dataclass(slots=True, frozen=True)
class PositionOpenedEvent(Event):
    position: Position

@dataclass(slots=True, frozen=True)
class PositionClosedEvent(Event):
    position: Position

@dataclass(slots=True, frozen=True)
class OrderFilledEvent(Event):
    order: PendingOrder

@dataclass(slots=True, frozen=True)
class OrderCancelledEvent(Event):
    order: PendingOrder
