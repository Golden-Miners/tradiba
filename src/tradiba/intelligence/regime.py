from typing import List
from tradiba.intelligence.models.allocation import CapitalAllocation
from tradiba.regimes.classifier import MarketRegime

class RegimeAwareAllocator:
    """
    Reference Implementation: Regime-Aware Allocator.
    Adjusts target weights based on the current market regime.
    """
    
    def __init__(self, base_allocations: List[CapitalAllocation]):
        self.base_allocations = base_allocations
        
    def adjust_for_regime(self, current_regime: MarketRegime) -> List[CapitalAllocation]:
        """Adjust allocations depending on whether strategies align with the regime."""
        adjusted = []
        
        for alloc in self.base_allocations:
            # Mock logic: Reduce allocation to everything if market is highly volatile
            # In a real system, we would match strategy risk_profile/type to the regime
            if current_regime == MarketRegime.VOLATILE:
                adjusted_weight = alloc.target_weight * 0.5
                adjusted_capital = alloc.capital * 0.5
            elif current_regime in (MarketRegime.TRENDING_UP, MarketRegime.TRENDING_DOWN):
                # E.g. favor trend following
                adjusted_weight = alloc.target_weight * 1.2
                adjusted_capital = alloc.capital * 1.2
            else:
                adjusted_weight = alloc.target_weight
                adjusted_capital = alloc.capital
                
            adjusted.append(CapitalAllocation(
                strategy_id=alloc.strategy_id,
                target_weight=adjusted_weight,
                capital=adjusted_capital,
                risk_budget=alloc.risk_budget
            ))
            
        # Re-normalize weights so they sum to 1.0 (if required by constraints)
        total_weight = sum(a.target_weight for a in adjusted)
        if total_weight > 0:
            for a in adjusted:
                a.target_weight /= total_weight
                
        return adjusted
