"""
Market structure domain events.
"""

from __future__ import annotations

from dataclasses import dataclass

from tradiba.events import Event

from .models import BreakOfStructure, ChangeOfCharacter, SwingHigh, SwingLow


@dataclass(frozen=True, slots=True)
class SwingHighDetectedEvent(Event):
    """Published when a swing high is confirmed."""

    swing: SwingHigh


@dataclass(frozen=True, slots=True)
class SwingLowDetectedEvent(Event):
    """Published when a swing low is confirmed."""

    swing: SwingLow


@dataclass(frozen=True, slots=True)
class BreakOfStructureEvent(Event):
    """Published when price breaks a level in the direction of the trend."""

    bos: BreakOfStructure


@dataclass(frozen=True, slots=True)
class ChangeOfCharacterEvent(Event):
    """Published when price breaks a level against the trend (potential reversal)."""

    choch: ChangeOfCharacter
