from dataclasses import dataclass

from .models import SwingPoint
from .models import Trend


@dataclass(slots=True)
class MarketStructureState:
    last_swing_high: SwingPoint | None = None
    last_swing_low: SwingPoint | None = None

    last_broken_high: float | None = None
    last_broken_low: float | None = None

    trend: Trend = Trend.UNKNOWN
