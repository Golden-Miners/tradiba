from typing import List, Dict
from tradiba.intelligence.models.strategy_descriptor import StrategyDescriptor

class ContinuousMonitor:
    """
    Reference Implementation: Continuous Monitoring.
    Tracks live strategy performance and triggers alerts/demotions if policies are breached.
    """
    
    def __init__(self, draw_down_limit: float = 0.15):
        self.draw_down_limit = draw_down_limit
        
    def check_health(self, active_strategies: List[StrategyDescriptor], latest_metrics: Dict[str, Dict[str, float]]) -> List[str]:
        """
        Check health of all active strategies against latest metrics.
        Returns a list of strategy IDs that need review/demotion.
        """
        flagged_strategies = []
        
        for strategy in active_strategies:
            metrics = latest_metrics.get(strategy.id, {})
            current_drawdown = metrics.get("max_drawdown", 0.0)
            
            # If a strategy breaches the global drawdown limit, flag it
            if current_drawdown > self.draw_down_limit:
                flagged_strategies.append(strategy.id)
                # In a real system, publish a PerformanceDriftAlertEvent
                
        return flagged_strategies
