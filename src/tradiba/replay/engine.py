from __future__ import annotations

from tradiba.events import EventBus

from .replay_clock import ReplayClock


class ReplayEngine:

    def __init__(
        self,
        event_bus: EventBus,
        clock: ReplayClock,
    ):
        self.event_bus = event_bus
        self.clock = clock

    def run(self):
        pass
