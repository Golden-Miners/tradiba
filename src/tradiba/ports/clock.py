from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime


class Clock(ABC):

    @abstractmethod
    def now(self) -> datetime:
        ...

_GLOBAL_CLOCK: Clock | None = None

def set_global_clock(clock: Clock) -> None:
    global _GLOBAL_CLOCK
    _GLOBAL_CLOCK = clock

def get_clock() -> Clock:
    global _GLOBAL_CLOCK
    if _GLOBAL_CLOCK is None:
        from tradiba.live.live_clock import LiveClock
        _GLOBAL_CLOCK = LiveClock()
    return _GLOBAL_CLOCK
