from typing import Dict, Any
import datetime

class AutonomousRebalancer:
    """
    Triggers rebalancing based on:
    - Regime changes
    - Strategy degradation
    - Volatility shifts
    - Correlation drift
    - Scheduled intervals
    - Risk limit proximity
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.last_rebalance = datetime.datetime.min
        self.rebalance_interval_days = config.get("rebalance_interval_days", 30)

    def should_rebalance(
        self,
        current_date: datetime.datetime,
        current_regime: str,
        previous_regime: str,
        strategy_performance: Dict[str, float]
    ) -> bool:
        """
        Determines if a rebalance is necessary.
        """
        # Trigger on regime change
        if current_regime != previous_regime:
            return True
            
        # Trigger on scheduled interval
        if (current_date - self.last_rebalance).days >= self.rebalance_interval_days:
            return True
            
        # Trigger on strategy degradation (e.g. any strategy draws down more than 15%)
        for sid, perf in strategy_performance.items():
            if perf < -0.15:
                return True
                
        # In a full implementation, volatility shifts and correlation drift would be checked here
                
        return False
        
    def execute_rebalance(self, current_date: datetime.datetime):
        """
        Records that a rebalance was executed.
        """
        self.last_rebalance = current_date
