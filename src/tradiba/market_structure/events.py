from dataclasses import dataclass

from tradiba.events import DomainEvent
from tradiba.market.models import Candle

from .models import SwingPoint, Trend, LiquidityPool, OrderBlock, FairValueGap
from .narrative import MarketNarrative

@dataclass(slots=True, frozen=True)
class MarketNarrativeUpdatedEvent(DomainEvent):
    narrative: MarketNarrative

@dataclass(slots=True, frozen=True)
class OrderBlockCreatedEvent(DomainEvent):
    block: OrderBlock


@dataclass(slots=True, frozen=True)
class OrderBlockTouchedEvent(DomainEvent):
    block: OrderBlock


@dataclass(slots=True, frozen=True)
class OrderBlockMitigatedEvent(DomainEvent):
    block: OrderBlock


@dataclass(slots=True, frozen=True)
class OrderBlockInvalidatedEvent(DomainEvent):
    block: OrderBlock


@dataclass(slots=True, frozen=True)
class LiquidityCreatedEvent(DomainEvent):
    pool: LiquidityPool


@dataclass(slots=True, frozen=True)
class LiquiditySweptEvent(DomainEvent):
    pool: LiquidityPool


@dataclass(slots=True, frozen=True)
class SwingHighEvent(DomainEvent):
    swing: SwingPoint


@dataclass(slots=True, frozen=True)
class SwingLowEvent(DomainEvent):
    swing: SwingPoint


@dataclass(slots=True, frozen=True)
class BullishBOSEvent(DomainEvent):
    candle: Candle
    broken_price: float


@dataclass(slots=True, frozen=True)
class BearishBOSEvent(DomainEvent):
    candle: Candle
    broken_price: float


@dataclass(slots=True, frozen=True)
class TrendChangedEvent(DomainEvent):
    previous: Trend
    current: Trend


@dataclass(slots=True, frozen=True)
class BullishCHOCHEvent(DomainEvent):
    candle: Candle
    broken_price: float


@dataclass(slots=True, frozen=True)
class BearishCHOCHEvent(DomainEvent):
    candle: Candle
    broken_price: float

@dataclass(slots=True, frozen=True)
class FairValueGapCreatedEvent(DomainEvent):
    gap: FairValueGap


@dataclass(slots=True, frozen=True)
class FairValueGapFilledEvent(DomainEvent):
    gap: FairValueGap


@dataclass(slots=True, frozen=True)
class FairValueGapInvalidatedEvent(DomainEvent):
    gap: FairValueGap


@dataclass(slots=True, frozen=True)
class FairValueGapArchivedEvent(DomainEvent):
    gap: FairValueGap
