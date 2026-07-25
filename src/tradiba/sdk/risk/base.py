from tradiba.sdk.plugin import Plugin
from tradiba.risk.base import RiskRule

class RiskRulePlugin(Plugin, RiskRule):
    """
    Base class for Risk Rule plugins.
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

    # From RiskRule
    # Subclasses must implement validate
