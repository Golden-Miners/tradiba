from dataclasses import dataclass

from tradiba.events import Event

from .models.order import Order


@dataclass(frozen=True, slots=True)
class OrderSubmittedEvent(Event):
    order: Order


@dataclass(frozen=True, slots=True)
class OrderFilledEvent(Event):
    order: Order


@dataclass(frozen=True, slots=True)
class OrderRejectedEvent(Event):
    order: Order
    reason: str
