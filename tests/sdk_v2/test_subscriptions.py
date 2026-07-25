from tradiba.sdk_v2.subscriptions import on
from tradiba.sdk_v2.strategy import Strategy

class SubbedStrategy(Strategy):
    @on("market.candle")
    def handle_candle(self, event):
        pass
        
    @on("market.trade")
    def handle_trade(self, event):
        pass

def test_subscriptions():
    strat = SubbedStrategy()
    
    assert hasattr(strat.handle_candle, "_subscriptions")
    assert "market.candle" in strat.handle_candle._subscriptions
    
    assert hasattr(strat.handle_trade, "_subscriptions")
    assert "market.trade" in strat.handle_trade._subscriptions
