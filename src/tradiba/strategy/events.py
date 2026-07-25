from dataclasses import dataclass
from .models import TradingSignal
from tradiba.events.event import DomainEvent

@dataclass(slots=True, frozen=True)
class TradingSignalCreatedEvent(DomainEvent):
    signal: TradingSignal
