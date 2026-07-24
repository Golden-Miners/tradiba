from __future__ import annotations

from tradiba.config import Settings

from .container import Container
from .lifecycle import Lifecycle


class Application:
    """Root application object."""

    def __init__(
        self,
        settings: Settings,
    ) -> None:
        self.settings = settings
        self.container = Container()
        self.lifecycle = Lifecycle()

        self.event_bus = None
        self.scheduler = None

        self.container.register_singleton(Application, self)

    def start(self) -> None:
        if self.lifecycle:
            self.lifecycle.start()
        if self.scheduler:
            self.scheduler.start()

    def stop(self) -> None:
        if self.scheduler:
            self.scheduler.stop()
        if self.lifecycle:
            self.lifecycle.stop()
