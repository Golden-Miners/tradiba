from tradiba.sdk.plugin import Plugin
from abc import abstractmethod
from typing import Any

class IndicatorPlugin(Plugin):
    """
    Base class for Indicator plugins.
    """
    @abstractmethod
    def update(self, candle: dict) -> None:
        """Update the indicator with a new candle."""
        pass

    @abstractmethod
    def value(self) -> Any:
        """Get the current value of the indicator."""
        pass

    # From Plugin
    def initialize(self, context):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def dispose(self):
        pass
