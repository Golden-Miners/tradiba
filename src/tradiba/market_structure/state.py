from dataclasses import dataclass, field

from .models import SwingPoint, Trend, LiquidityPool


@dataclass(slots=True)
class MarketStructureState:
    last_swing_high: SwingPoint | None = None
    last_swing_low: SwingPoint | None = None

    last_broken_high: float | None = None
    last_broken_low: float | None = None

    choch_detected: bool = False

    trend: Trend = Trend.UNKNOWN

    active_liquidity: list[LiquidityPool] = field(default_factory=list)
