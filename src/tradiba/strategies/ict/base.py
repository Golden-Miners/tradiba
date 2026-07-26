from dataclasses import dataclass
from typing import Optional

@dataclass
class StrategyRiskProfile:
    max_drawdown_pct: float
    max_position_size_pct: float
    stop_loss_pct: float
    take_profit_pct: Optional[float] = None

@dataclass
class StrategyMetadata:
    id: str
    name: str
    description: str
    author: str
    version: str
    required_timeframes: list[str]
    risk_profile: StrategyRiskProfile
