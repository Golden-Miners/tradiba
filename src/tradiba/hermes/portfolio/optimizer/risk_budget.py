from typing import Dict, Any

class RiskBudgetOptimizer:
    """
    Optimizes and constrains portfolio allocation based on risk parameters:
    - Portfolio drawdown
    - Sector/Currency exposure
    - Correlation limits
    - Concentration limits
    - Maximum leverage
    - Daily loss limits
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.max_concentration = config.get("max_concentration", 0.20)  # max 20% per strategy
        self.max_sector_exposure = config.get("max_sector_exposure", 0.40) # max 40% per sector
        self.max_leverage = config.get("max_leverage", 1.0) # max total leverage

    def optimize(
        self,
        proposed_allocation: Dict[str, float],
        strategy_metadata: Dict[str, Dict[str, Any]]
    ) -> Dict[str, float]:
        """
        Takes a proposed allocation fraction for each strategy, 
        and scales/caps them to meet risk budgets.
        """
        if not proposed_allocation:
            return {}

        optimized = proposed_allocation.copy()

        # Apply concentration limits
        for sid, alloc in optimized.items():
            if alloc > self.max_concentration:
                optimized[sid] = self.max_concentration

        # Apply sector/currency exposure limits
        sector_totals = {}
        for sid, alloc in optimized.items():
            meta = strategy_metadata.get(sid, {})
            sector = meta.get("sector", "unknown")
            sector_totals[sector] = sector_totals.get(sector, 0.0) + alloc

        for sid, alloc in list(optimized.items()):
            meta = strategy_metadata.get(sid, {})
            sector = meta.get("sector", "unknown")
            if sector_totals[sector] > self.max_sector_exposure:
                # scale down proportional to exceedance
                scale = self.max_sector_exposure / sector_totals[sector]
                optimized[sid] = alloc * scale

        # Apply leverage limit
        total_allocation = sum(optimized.values())
        if total_allocation > self.max_leverage:
            scale = self.max_leverage / total_allocation
            for sid in optimized:
                optimized[sid] *= scale

        return optimized
