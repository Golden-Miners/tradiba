from tradiba.intelligence.models.strategy_descriptor import StrategyDescriptor, StrategyStatus
from tradiba.intelligence.governance import GovernanceGate

class StrategyLifecycleManager:
    """
    Reference Implementation: Strategy Lifecycle Manager.
    Moves strategies through the pipeline (Experimental -> Production -> Retired).
    """
    def __init__(self, governance: GovernanceGate):
        self.governance = governance
        
    def promote(self, strategy: StrategyDescriptor, target_status: StrategyStatus) -> bool:
        """Attempt to promote the strategy to the target status."""
        if self.governance.can_promote(strategy, target_status):
            strategy.status = target_status
            # In a real system, publish a StrategyPromotedEvent here
            return True
        return False
        
    def retire(self, strategy: StrategyDescriptor):
        """Retire a strategy from active trading."""
        strategy.status = StrategyStatus.RETIRED
        # Publish StrategyRetiredEvent
