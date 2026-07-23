"""
Tradiba application.
"""

from __future__ import annotations

from tradiba.config import Settings, load_settings
from tradiba.events import EventBus
from tradiba.mt5 import MT5Service
from tradiba.scheduler import Scheduler

from .container import Container
from .lifecycle import Lifecycle


class Application:
    def __init__(self) -> None:
        self.settings: Settings = load_settings()
        self.container = Container()
        self.lifecycle = Lifecycle()

        self.event_bus = EventBus()
        self.scheduler = Scheduler()
        self.mt5 = MT5Service()

        self.container.register_singleton(Application, self)
        self.container.register_singleton(EventBus, self.event_bus)
        self.container.register_singleton(Scheduler, self.scheduler)
        self.container.register_singleton(MT5Service, self.mt5)

        self.lifecycle.add(self.mt5)

    def start(self) -> None:
        self.lifecycle.start()

    def stop(self) -> None:
        self.scheduler.stop()
        self.lifecycle.stop()
