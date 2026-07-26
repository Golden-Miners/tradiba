from dataclasses import dataclass
from tradiba.events.event import DomainEvent
from tradiba.intelligence.models.strategy_descriptor import StrategyStatus

@dataclass(frozen=True)
class StrategyPromotedEvent(DomainEvent):
    strategy_id: str
    previous_status: StrategyStatus
    new_status: StrategyStatus

@dataclass(frozen=True)
class StrategyRetiredEvent(DomainEvent):
    strategy_id: str
    reason: str

@dataclass(frozen=True)
class PortfolioRebalancedEvent(DomainEvent):
    portfolio_id: str
    num_strategies_allocated: int
    total_capital_allocated: float

@dataclass(frozen=True)
class StrategyScoreUpdatedEvent(DomainEvent):
    strategy_id: str
    new_composite_score: float
