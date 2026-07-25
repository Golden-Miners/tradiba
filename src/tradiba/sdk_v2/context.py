from typing import Any
from dataclasses import dataclass, field
from tradiba.sdk_v2.narrative import MarketNarrative

@dataclass(frozen=True)
class PortfolioContext:
    """Provides read-only access to portfolio state."""
    cash: float = 0.0
    equity: float = 0.0
    positions: dict[str, Any] = field(default_factory=dict)
    
@dataclass(frozen=True)
class RiskContext:
    """Provides read-only access to risk limits."""
    max_drawdown_pct: float = 0.0
    max_position_size: float = 0.0
    
@dataclass(frozen=True)
class MarketContext:
    """Provides access to market data and narrative."""
    narrative: MarketNarrative = field(default_factory=MarketNarrative)
    
@dataclass(frozen=True)
class StrategyContext:
    """
    The canonical, strongly-typed context passed to all Strategy SDK v2 hooks.
    Replaces global service lookups.
    """
    portfolio: PortfolioContext = field(default_factory=PortfolioContext)
    risk: RiskContext = field(default_factory=RiskContext)
    market: MarketContext = field(default_factory=MarketContext)
    clock: float = 0.0
    logger: Any = None
    metrics: Any = None
    configuration: dict[str, Any] = field(default_factory=dict)
