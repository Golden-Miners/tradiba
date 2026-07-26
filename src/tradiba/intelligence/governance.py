from typing import Protocol
from tradiba.intelligence.models.strategy_descriptor import StrategyDescriptor, StrategyStatus

class GovernanceGate(Protocol):
    """Protocol for checking if a strategy is allowed to advance to the next state."""
    
    def can_promote(self, strategy: StrategyDescriptor, target_status: StrategyStatus) -> bool:
        ...

class StandardGovernance:
    """
    Reference Implementation: Governance.
    Checks basic rules before promoting strategies.
    """
    def can_promote(self, strategy: StrategyDescriptor, target_status: StrategyStatus) -> bool:
        # Mock logic
        if target_status == StrategyStatus.PRODUCTION:
            return strategy.status == StrategyStatus.PAPER_TRADING
        return True
