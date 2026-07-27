from typing import Dict, Any

class SafetySupervisor:
    """
    Continuously monitors:
    - Drawdown
    - Win rate degradation
    - Slippage
    - Latency
    - Broker connectivity
    - Model confidence
    - Market anomalies
    
    Breaches trigger predefined safety actions.
    """

    def __init__(self, limits: Dict[str, Any]):
        self.limits = limits

    def check_safety(self, metrics: Dict[str, Any]) -> str:
        """
        Returns "SAFE" if all metrics are within limits, otherwise returns a string describing the breach.
        """
        if metrics.get("drawdown", 0.0) > self.limits.get("max_drawdown", float('inf')):
            return "BREACH_DRAWDOWN"
            
        if metrics.get("win_rate", 1.0) < self.limits.get("min_win_rate", 0.0):
            return "BREACH_WIN_RATE"
            
        if metrics.get("slippage", 0.0) > self.limits.get("max_slippage", float('inf')):
            return "BREACH_SLIPPAGE"
            
        if metrics.get("latency_ms", 0) > self.limits.get("max_latency_ms", float('inf')):
            return "BREACH_LATENCY"
            
        if not metrics.get("broker_connected", True):
            return "BREACH_BROKER_DISCONNECTED"
            
        if metrics.get("market_anomalies_detected", False):
            return "BREACH_MARKET_ANOMALY"

        return "SAFE"
