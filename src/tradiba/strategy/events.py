"""
Strategy domain events.
"""

from __future__ import annotations

from dataclasses import dataclass

from tradiba.events import Event

from .models import Signal


@dataclass(frozen=True, slots=True)
class SignalGeneratedEvent(Event):
    """Published when a strategy generates a new trading signal."""

    signal: Signal


@dataclass(frozen=True, slots=True)
class SignalRejectedEvent(Event):
    """Published when a signal is rejected (e.g., by risk management)."""

    signal: Signal
    reason: str


@dataclass(frozen=True, slots=True)
class SignalExpiredEvent(Event):
    """Published when a pending signal is no longer valid."""

    signal: Signal
