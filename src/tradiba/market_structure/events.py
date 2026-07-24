from dataclasses import dataclass

from tradiba.events import Event
from tradiba.market.models import Candle

from .models import SwingPoint, Trend, LiquidityPool, OrderBlock
from .narrative import MarketNarrative

@dataclass(slots=True, frozen=True)
class MarketNarrativeUpdatedEvent(Event):
    narrative: MarketNarrative

@dataclass(slots=True, frozen=True)
class OrderBlockCreatedEvent(Event):
    block: OrderBlock


@dataclass(slots=True, frozen=True)
class OrderBlockTouchedEvent(Event):
    block: OrderBlock


@dataclass(slots=True, frozen=True)
class OrderBlockMitigatedEvent(Event):
    block: OrderBlock


@dataclass(slots=True, frozen=True)
class OrderBlockInvalidatedEvent(Event):
    block: OrderBlock


@dataclass(slots=True, frozen=True)
class LiquidityCreatedEvent(Event):
    pool: LiquidityPool


@dataclass(slots=True, frozen=True)
class LiquiditySweptEvent(Event):
    pool: LiquidityPool


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
