from typing import List
from tradiba.intelligence.allocation import PortfolioConstructor
from tradiba.intelligence.models.allocation import CapitalAllocation
from tradiba.intelligence.scoring import StrategyScorecard

class EqualWeightAllocator(PortfolioConstructor):
    """
    Reference Implementation: Equal Weight Allocator.
    Assigns an equal portion of capital to all provided strategies.
    """
    def allocate(self, scorecards: List[StrategyScorecard], total_capital: float) -> List[CapitalAllocation]:
        if not scorecards:
            return []
            
        weight = 1.0 / len(scorecards)
        capital_per_strategy = total_capital * weight
        
        allocations = []
        for card in scorecards:
            allocations.append(CapitalAllocation(
                strategy_id=card.strategy_id,
                target_weight=weight,
                capital=capital_per_strategy,
                risk_budget={"max_drawdown": capital_per_strategy * 0.1} # Mock 10% risk budget
            ))
            
        return allocations

class VolatilityTargetingAllocator(PortfolioConstructor):
    """
    Reference Implementation: Volatility Targeting Allocator.
    Adjusts weights inversely proportional to strategy volatility.
    """
    def allocate(self, scorecards: List[StrategyScorecard], total_capital: float) -> List[CapitalAllocation]:
        # For this reference implementation, we use inverse of Var95 as a proxy for inverse volatility
        # If var_95 is 0, we assign a very small weight to avoid division by zero.
        total_inv_vol = 0.0
        inv_vols = []
        
        for card in scorecards:
            inv_vol = 1.0 / (card.var_95 if card.var_95 > 0 else 1.0)
            inv_vols.append(inv_vol)
            total_inv_vol += inv_vol
            
        allocations = []
        for i, card in enumerate(scorecards):
            weight = inv_vols[i] / total_inv_vol if total_inv_vol > 0 else 0
            capital = total_capital * weight
            allocations.append(CapitalAllocation(
                strategy_id=card.strategy_id,
                target_weight=weight,
                capital=capital,
                risk_budget={"var_95_limit": card.var_95}
            ))
            
        return allocations
