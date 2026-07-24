from dataclasses import dataclass
from tradiba.events import Event
from .models import Portfolio

@dataclass(frozen=True, slots=True)
class PortfolioUpdatedEvent(Event):
    portfolio: Portfolio

@dataclass(frozen=True, slots=True)
class PositionClosedEvent(Event):
    ticket: int
    symbol: str
    side: str
    volume: float
    entry: float
    exit: float
    profit: float
