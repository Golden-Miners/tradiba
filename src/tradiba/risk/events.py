from dataclasses import dataclass
from tradiba.events import Event
from .models import TradePlan

@dataclass(slots=True, frozen=True)
class TradeApprovedEvent(Event):
    plan: TradePlan

@dataclass(slots=True, frozen=True)
class TradeRejectedEvent(Event):
    plan: TradePlan
