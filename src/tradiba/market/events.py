"""
Market data domain events.
"""

from __future__ import annotations

from dataclasses import dataclass

from tradiba.events import Event
from tradiba.mt5.models import Candle, Tick


@dataclass(frozen=True, slots=True)
class TickReceivedEvent(Event):
    """Published when a new (deduplicated) market tick arrives."""

    tick: Tick


@dataclass(frozen=True, slots=True)
class CandleClosedEvent(Event):
    """Published when a timeframe bar completes."""

    candle: Candle


@dataclass(frozen=True, slots=True)
class SymbolConnectedEvent(Event):
    """Published when a symbol subscription is added."""

    symbol: str


@dataclass(frozen=True, slots=True)
class SymbolDisconnectedEvent(Event):
    """Published when a symbol subscription is removed."""

    symbol: str
