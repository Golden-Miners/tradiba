from dataclasses import dataclass
from typing import Dict


@dataclass(slots=True)
class OptimizationStatistics:
    """Contains the performance statistics of a single backtest run."""
    net_profit: float
    total_trades: int
    win_rate: float
    profit_factor: float
    max_drawdown: float
    sharpe_ratio: float
    sortino_ratio: float
    calmar_ratio: float


@dataclass(slots=True)
class OptimizationResult:
    """The complete result of evaluating one parameter set."""
    parameters: Dict[str, float]
    statistics: OptimizationStatistics
    score: float = 0.0
