from dataclasses import dataclass

from tradiba.events import Event
from tradiba.market.models import Candle

from .models import SwingPoint, Trend


@dataclass(slots=True, frozen=True)
class SwingHighEvent(Event):
    swing: SwingPoint


@dataclass(slots=True, frozen=True)
class SwingLowEvent(Event):
    swing: SwingPoint


@dataclass(slots=True, frozen=True)
class BullishBOSEvent(Event):
    candle: Candle
    broken_price: float


@dataclass(slots=True, frozen=True)
class BearishBOSEvent(Event):
    candle: Candle
    broken_price: float


@dataclass(slots=True, frozen=True)
class TrendChangedEvent(Event):
    previous: Trend
    current: Trend


@dataclass(slots=True, frozen=True)
class BullishCHOCHEvent(Event):
    candle: Candle
    broken_price: float


@dataclass(slots=True, frozen=True)
class BearishCHOCHEvent(Event):
    candle: Candle
    broken_price: float
