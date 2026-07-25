from abc import ABC, abstractmethod
from typing import Any
import logging

from tradiba.events.bus import EventBus
from tradiba.config.settings import Settings

class PluginContext:
    """
    Context provided to plugins during initialization.
    Exposes safe platform services.
    """
    def __init__(
        self,
        logger: logging.Logger,
        event_bus: EventBus,
        configuration: Settings,
        metrics: Any,
        services: dict[str, Any]
    ):
        self.logger = logger
        self.event_bus = event_bus
        self.configuration = configuration
        self.metrics = metrics
        self.services = services


class Plugin(ABC):
    """
    Base Plugin Interface for all Tradiba plugins.
    """

    @abstractmethod
    def initialize(self, context: PluginContext) -> None:
        """Called once when the plugin is loaded."""
        pass

    @abstractmethod
    def start(self) -> None:
        """Called to activate the plugin."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Called to deactivate the plugin."""
        pass

    @abstractmethod
    def dispose(self) -> None:
        """Called when the plugin is unloaded for cleanup."""
        pass
