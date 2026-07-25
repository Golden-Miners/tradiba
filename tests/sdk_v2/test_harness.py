from tradiba.sdk_v2.simulation import StrategyHarness
from tradiba.sdk_v2.strategy import Strategy
from tradiba.sdk_v2.subscriptions import on

class TestStrat(Strategy):
    def __init__(self):
        super().__init__()
        self.count = 0
        
    @on("candle")
    def on_candle(self, event):
        self.count += 1

def test_harness_routing():
    strat = TestStrat()
    harness = StrategyHarness(strat)
    
    # Should route to on_candle
    harness.feed("candle", {"price": 100})
    assert strat.count == 1
    
    # Unsubscribed event
    harness.feed("unknown", {"price": 100})
    assert strat.count == 1
    
    # Harness initializes the context
    assert strat.ctx is not None
