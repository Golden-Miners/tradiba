"""
Market data subscription definitions.
"""

from __future__ import annotations

from dataclasses import dataclass

from tradiba.mt5.timeframes import Timeframe


@dataclass(frozen=True, slots=True)
class Subscription:
    """Describes a symbol being monitored at a specific timeframe."""

    symbol: str
    timeframe: Timeframe
