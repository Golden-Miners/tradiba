from dataclasses import dataclass
from .models import TradingSignal
from tradiba.events.base import Event

@dataclass(slots=True, frozen=True)
class TradingSignalCreatedEvent(Event):
    signal: TradingSignal
