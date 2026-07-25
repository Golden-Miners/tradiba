from dataclasses import dataclass
from tradiba.events import DomainEvent
from .models import TradePlan

@dataclass(slots=True, frozen=True)
class TradeApprovedEvent(DomainEvent):
    plan: TradePlan

@dataclass(slots=True, frozen=True)
class TradeRejectedEvent(DomainEvent):
    plan: TradePlan
