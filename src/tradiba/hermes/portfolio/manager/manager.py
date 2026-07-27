from typing import Dict, Any, List
import datetime

from tradiba.events import EventBus
from tradiba.hermes.events import (
    HermesAllocationProposedEvent,
    HermesRebalanceRequestedEvent
)
from tradiba.hermes.portfolio.allocator.dynamic_allocator import DynamicAllocator
from tradiba.hermes.portfolio.optimizer.risk_budget import RiskBudgetOptimizer
from tradiba.hermes.portfolio.rebalancer.autonomous_rebalancer import AutonomousRebalancer
from tradiba.hermes.portfolio.supervisor.cross_strategy import CrossStrategyCoordinator
from tradiba.hermes.portfolio.learning.portfolio_learning import PortfolioLearningEngine
from tradiba.hermes.portfolio.governance.workflow import GovernanceWorkflow
from tradiba.hermes.portfolio.attribution.performance import PerformanceAttribution
from tradiba.hermes.portfolio.reports.generator import PortfolioReportGenerator

class PortfolioManagerAgent:
    """
    Hermes autonomously:
    - Selects strategies
    - Allocates capital
    - Adjusts exposure
    - Monitors portfolio health
    - Initiates rebalancing proposals
    
    All actions occur only in Digital Twin and Paper Trading.
    """

    def __init__(self, config: Dict[str, Any], event_bus: EventBus):
        self.config = config
        self.event_bus = event_bus
        
        self.allocator = DynamicAllocator(config)
        self.optimizer = RiskBudgetOptimizer(config)
        self.rebalancer = AutonomousRebalancer(config)
        self.supervisor = CrossStrategyCoordinator(config)
        self.learning = PortfolioLearningEngine(config)
        self.governance = GovernanceWorkflow(config)
        self.attribution = PerformanceAttribution(config)
        self.reporter = PortfolioReportGenerator(config)

    def manage_portfolio(
        self,
        current_date: datetime.datetime,
        available_strategies: List[Dict[str, Any]],
        correlation_matrix: Dict[str, Dict[str, float]],
        strategy_metadata: Dict[str, Dict[str, Any]],
        current_regime: str,
        previous_regime: str,
        strategy_performance: Dict[str, float]
    ) -> Dict[str, float]:
        """
        Main entry point for autonomous portfolio management.
        """
        # 1. Filter out overlapping strategies
        selected_strategies = self.supervisor.evaluate_interactions(
            available_strategies, 
            correlation_matrix
        )

        # 2. Check if rebalance is needed
        needs_rebalance = self.rebalancer.should_rebalance(
            current_date,
            current_regime,
            previous_regime,
            strategy_performance
        )

        if needs_rebalance:
            self.event_bus.publish(HermesRebalanceRequestedEvent(
                timestamp=current_date.timestamp(),
                payload={"reason": "rebalance criteria met"}
            ))
            self.rebalancer.execute_rebalance(current_date)

        # 3. Propose allocation
        raw_allocation = self.allocator.allocate(selected_strategies, current_regime)

        # 4. Optimize against risk budgets
        optimized_allocation = self.optimizer.optimize(
            raw_allocation, 
            strategy_metadata
        )

        proposal = {
            "proposed_allocation": optimized_allocation,
            "regime": current_regime
        }

        self.event_bus.publish(HermesAllocationProposedEvent(
            timestamp=current_date.timestamp(),
            payload=proposal
        ))

        # 5. Governance check
        # Mock risk engine approval = True for simulation
        is_approved = self.governance.approve_proposal(proposal, risk_approved=True)
        
        if is_approved:
            # Execute in non-live environments
            pass
        else:
            # Blocked (e.g. if it's Live environment)
            pass

        return optimized_allocation
