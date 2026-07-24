from dataclasses import dataclass

from tradiba.events import Event
from tradiba.strategy.models import Signal


@dataclass(frozen=True, slots=True)
class RiskApprovedEvent(Event):
    signal: Signal


@dataclass(frozen=True, slots=True)
class RiskRejectedEvent(Event):
    signal: Signal
    reason: str
