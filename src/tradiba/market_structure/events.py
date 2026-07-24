from dataclasses import dataclass

from tradiba.events import Event
from .models import SwingPoint


@dataclass(slots=True, frozen=True)
class SwingHighEvent(Event):
    swing: SwingPoint


@dataclass(slots=True, frozen=True)
class SwingLowEvent(Event):
    swing: SwingPoint
