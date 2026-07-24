"""
Market structure domain events.
"""

from __future__ import annotations

from dataclasses import dataclass

from tradiba.events import Event
from tradiba.mt5.models import Candle

from .models import BreakOfStructure, ChangeOfCharacter, SwingPoint, Trend, LiquidityPool, FairValueGap, OrderBlock


@dataclass(frozen=True, slots=True)
class SwingHighEvent(Event):
    """Published when a swing high is confirmed."""
    swing: SwingPoint


@dataclass(frozen=True, slots=True)
class SwingLowEvent(Event):
    """Published when a swing low is confirmed."""
    swing: SwingPoint


@dataclass(frozen=True, slots=True)
class TrendChangedEvent(Event):
    """Published when the overall market trend changes."""
    symbol: str
    timeframe: str
    old_trend: Trend
    new_trend: Trend


@dataclass(frozen=True, slots=True)
class BOSEvent(Event):
    """Published when price breaks a level in the direction of the trend."""
    symbol: str
    direction: Trend
    broken_price: float
    candle: Candle
    bos: BreakOfStructure


@dataclass(frozen=True, slots=True)
class CHOCHEvent(Event):
    """Published when price breaks a level against the trend (potential reversal)."""
    choch: ChangeOfCharacter


# ---------------------------------------------------------------------------
# Liquidity events
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class LiquidityCreatedEvent(Event):
    """Published when a new liquidity pool is identified."""
    pool: LiquidityPool


@dataclass(frozen=True, slots=True)
class LiquiditySweptEvent(Event):
    """Published when a liquidity pool is swept by price."""
    pool: LiquidityPool
    candle: Candle


@dataclass(frozen=True, slots=True)
class LiquidityPoolArchivedEvent(Event):
    """Published when a liquidity pool is invalidated/archived."""
    pool: LiquidityPool


# ---------------------------------------------------------------------------
# Fair Value Gap events
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class FairValueGapCreatedEvent(Event):
    """Published when a new Fair Value Gap forms."""
    symbol: str
    timeframe: str
    fvg: FairValueGap


@dataclass(frozen=True, slots=True)
class FairValueGapFilledEvent(Event):
    """Published when a Fair Value Gap is completely filled."""
    symbol: str
    timeframe: str
    fvg: FairValueGap


@dataclass(frozen=True, slots=True)
class FairValueGapArchivedEvent(Event):
    """Published when a Fair Value Gap expires (too old without being touched)."""
    symbol: str
    timeframe: str
    fvg: FairValueGap


# ---------------------------------------------------------------------------
# Order Block events
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class OrderBlockCreatedEvent(Event):
    """Published when a valid Order Block is formed from a Break of Structure."""
    ob: OrderBlock


@dataclass(frozen=True, slots=True)
class OrderBlockFilledEvent(Event):
    """Published when an Order Block is fully mitigated/filled."""
    ob: OrderBlock


@dataclass(frozen=True, slots=True)
class OrderBlockArchivedEvent(Event):
    """Published when an Order Block is invalidated/archived."""
    ob: OrderBlock
