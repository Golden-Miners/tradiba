from tradiba.sdk_v2.strategy import Strategy
from tradiba.sdk_v2.parameters import FloatParameter, IntParameter
from tradiba.sdk_v2.subscriptions import on
from tradiba.sdk_v2.indicators import SMA

class TrendFollowingStrategy(Strategy):
    """
    Classic trend following using SMA crossovers.
    """
    fast_window = IntParameter(default=10, minimum=5)
    slow_window = IntParameter(default=30, minimum=20)
    risk_percent = FloatParameter(default=1.0, minimum=0.5, maximum=2.0)
    
    def on_initialize(self, ctx):
        self.fast_sma = SMA(window=self.fast_window) # type: ignore
        self.slow_sma = SMA(window=self.slow_window) # type: ignore
        
    @on("candle")
    def on_candle(self, event):
        self.fast_sma.update(event["close"])
        self.slow_sma.update(event["close"])
        
        # In a real strategy, this would emit an order via ctx.portfolio
