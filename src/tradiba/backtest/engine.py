from typing import Optional
from datetime import datetime

from tradiba.events import EventBus
from tradiba.market.events import CandleClosedEvent

from .feed import HistoricalCSVFeed
from .executor import PaperExecutionAdapter


class BacktestEngine:
    """
    Orchestrates the backtest simulation by pumping historical data through the event bus
    and stepping the simulated execution adapter.
    """
    
    def __init__(self, 
                 feed: HistoricalCSVFeed, 
                 event_bus: EventBus, 
                 executor: PaperExecutionAdapter):
        self.feed = feed
        self.event_bus = event_bus
        self.executor = executor
        self.current_time: Optional[datetime] = None
        
        # We hook into CandleClosedEvent to step our simulated executor
        self.event_bus.subscribe(CandleClosedEvent, self._on_candle_closed)
        
    def _on_candle_closed(self, event: CandleClosedEvent) -> None:
        c = event.candle
        self.current_time = c.time
        
        # Step the executor to check for fills and SL/TP
        self.executor.simulate_candle(high=c.high, low=c.low, close=c.close)
        
    def run(self) -> dict:
        """
        Runs the simulation to completion.
        Returns basic statistics.
        """
        for event in self.feed.read_events():
            # In a synchronous EventBus, publishing an event immediately calls handlers.
            self.event_bus.publish(event)
            
        info = self.executor.account_info()
        return {
            "initial_balance": self.executor._initial_balance,
            "final_balance": info.balance,
            "net_profit": info.balance - self.executor._initial_balance,
            "final_equity": info.equity,
        }
