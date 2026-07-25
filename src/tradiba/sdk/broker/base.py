from tradiba.sdk.plugin import Plugin
from tradiba.execution.broker import BrokerExecutor

class BrokerPlugin(Plugin, BrokerExecutor):
    """
    Base class for Broker plugins.
    """
    # From Plugin
    def initialize(self, context):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def dispose(self):
        pass

    # From BrokerExecutor
    # Subclasses must implement submit, modify, cancel, synchronize
