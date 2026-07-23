"""
Tradiba application.
"""

from __future__ import annotations

from tradiba.config import Settings, load_settings

from .bootstrap import bootstrap
from .container import Container
from .lifecycle import Lifecycle


class Application:

    def __init__(self) -> None:
        self.settings: Settings = load_settings()

        self.container = Container()
        self.lifecycle = Lifecycle()

        services = bootstrap(
            self.container,
            self.lifecycle,
        )

        self.event_bus = services.event_bus
        self.scheduler = services.scheduler
        self.mt5 = services.mt5

        self.container.register_singleton(
            Application,
            self,
        )

    def start(self) -> None:
        self.lifecycle.start()

    def stop(self) -> None:
        self.scheduler.stop()
        self.lifecycle.stop()