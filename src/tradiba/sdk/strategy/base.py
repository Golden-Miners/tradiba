from tradiba.sdk.plugin import Plugin
from tradiba.strategy.interface import Strategy

class StrategyPlugin(Plugin, Strategy):
    """
    Base class for Strategy plugins.
    Inherits from both the Plugin lifecycle interface and the core Strategy interface.
    """
    def __init__(self, name: str, priority: int = 100, enabled: bool = True):
        super().__init__()
        self.name = name
        self.priority = priority
        self.enabled = enabled

    # From Plugin
    def initialize(self, context):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def dispose(self):
        pass

    # From Strategy
    # Subclasses must implement evaluate
