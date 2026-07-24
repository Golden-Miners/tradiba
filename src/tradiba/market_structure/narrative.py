from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum

from .models import (
    Trend,
    LiquidityPool,
    FairValueGap,
    OrderBlock,
)

class MarketBias(Enum):
    STRONG_BULLISH = 5
    BULLISH = 4
    NEUTRAL = 3
    BEARISH = 2
    STRONG_BEARISH = 1

@dataclass(slots=True, frozen=True)
class MarketNarrative:
    symbol: str
    timeframe: str
    trend: Trend
    bias: MarketBias
    confidence: int = 0
    premium_discount: float = 0.5
    liquidity: tuple[LiquidityPool, ...] = field(default_factory=tuple)
    fvgs: tuple[FairValueGap, ...] = field(default_factory=tuple)
    order_blocks: tuple[OrderBlock, ...] = field(default_factory=tuple)
