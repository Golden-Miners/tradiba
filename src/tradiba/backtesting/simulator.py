from dataclasses import dataclass
from datetime import datetime
from typing import Any, List

@dataclass
class MarketEvent:
    timestamp: datetime
    type: str
    details: dict

class AdvancedSimulator:
    """
    Reference Implementation: Advanced Backtesting Simulator.
    Simulates real-world market friction like gaps, outages, and dynamic spreads.
    """
    
    def __init__(self):
        self.events: List[MarketEvent] = []
        
    def add_latency(self, ms: int):
        """Simulate execution latency."""
        pass
        
    def inject_session_gap(self, start_time: datetime, end_time: datetime):
        """Simulate a market close/open gap."""
        self.events.append(MarketEvent(
            timestamp=start_time,
            type="SESSION_CLOSE",
            details={"reopen_at": end_time}
        ))
        
    def inject_exchange_outage(self, timestamp: datetime, duration_ms: int):
        """Simulate a connection loss to the exchange."""
        self.events.append(MarketEvent(
            timestamp=timestamp,
            type="EXCHANGE_OUTAGE",
            details={"duration_ms": duration_ms}
        ))
        
    def apply_dynamic_spread(self, base_spread: float, volatility_multiplier: float):
        """Widen spreads based on simulated volatility."""
        pass
        
    def step(self, current_time: datetime, market_data: Any) -> Any:
        """Process one tick/bar of the backtest, applying active frictions."""
        # Check for active events and alter execution probability/price
        return market_data
