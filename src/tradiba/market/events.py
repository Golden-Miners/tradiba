from dataclasses import dataclass

from .models import Candle, Tick
from tradiba.events import DomainEvent


@dataclass(slots=True, frozen=True)
class CandleClosedEvent(DomainEvent):
    candle: Candle


@dataclass(slots=True, frozen=True)
class CandleUpdatedEvent(DomainEvent):
    candle: Candle


@dataclass(slots=True, frozen=True)
class TickEvent(DomainEvent):
    tick: Tick


@dataclass(slots=True, frozen=True)
class SymbolConnectedEvent(DomainEvent):
    symbol: str


@dataclass(slots=True, frozen=True)
class SymbolDisconnectedEvent(DomainEvent):
    symbol: str
