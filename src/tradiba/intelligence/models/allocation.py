from dataclasses import dataclass
from typing import Dict

@dataclass
class CapitalAllocation:
    """
    Reference Implementation: Capital Allocation.
    Represents the target state for a specific strategy within the portfolio.
    """
    strategy_id: str
    target_weight: float
    capital: float
    risk_budget: Dict[str, float]  # e.g., {"max_drawdown": 5000, "var_95": 1000}
