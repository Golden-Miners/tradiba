from dataclasses import dataclass

@dataclass
class PortfolioConfiguration:
    """Global configuration for portfolio intelligence constraints."""
    max_strategy_weight: float = 0.25
    global_drawdown_limit: float = 0.15
    rebalance_frequency_hours: int = 24
