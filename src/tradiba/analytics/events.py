from dataclasses import dataclass
from tradiba.events.event import DomainEvent

@dataclass(frozen=True)
class PortfolioAnalyticsUpdatedEvent(DomainEvent):
    """Fired when portfolio analytics (exposures, VaR, correlations) are updated."""
    snapshot_timestamp: str
    var_95: float
    expected_shortfall_95: float

@dataclass(frozen=True)
class RiskLimitBreachedEvent(DomainEvent):
    """Fired when a portfolio-level risk limit is breached."""
    limit_name: str
    current_value: float
    threshold: float
    breach_type: str # "hard" or "soft"

@dataclass(frozen=True)
class StressTestCompletedEvent(DomainEvent):
    """Fired when stress test scenarios complete their evaluation."""
    scenario_name: str
    projected_loss: float

@dataclass(frozen=True)
class AllocationRecommendationCreatedEvent(DomainEvent):
    """Fired when the optimizer produces a new capital allocation recommendation."""
    strategy_allocations: dict[str, float]
