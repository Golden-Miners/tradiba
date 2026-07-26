from typing import List, Protocol
from tradiba.intelligence.models.allocation import CapitalAllocation
from tradiba.intelligence.scoring import StrategyScorecard

class PortfolioConstructor(Protocol):
    """Protocol for constructing a portfolio from a list of strategy scorecards."""
    
    def allocate(self, scorecards: List[StrategyScorecard], total_capital: float) -> List[CapitalAllocation]:
        """Generate capital allocations for the given strategies."""
        ...

class CapitalAllocationEngine:
    """
    Reference Implementation: Capital Allocation Engine.
    Orchestrates the portfolio construction process.
    """
    def __init__(self, allocator: PortfolioConstructor):
        self.allocator = allocator
        
    def rebalance(self, active_scorecards: List[StrategyScorecard], total_capital: float) -> List[CapitalAllocation]:
        """Rebalance the portfolio and return the new target allocations."""
        if not active_scorecards:
            return []
            
        allocations = self.allocator.allocate(active_scorecards, total_capital)
        
        # In a real system, apply max capacity constraints, regulatory limits, etc. here.
        return allocations
