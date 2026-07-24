from dataclasses import dataclass

from .models import Candle, Tick
from tradiba.events import Event


@dataclass(slots=True, frozen=True)
class CandleClosedEvent(Event):
    candle: Candle


@dataclass(slots=True, frozen=True)
class CandleUpdatedEvent(Event):
    candle: Candle


@dataclass(slots=True, frozen=True)
class TickEvent(Event):
    tick: Tick


@dataclass(slots=True, frozen=True)
class SymbolConnectedEvent(Event):
    symbol: str


@dataclass(slots=True, frozen=True)
class SymbolDisconnectedEvent(Event):
    symbol: str
