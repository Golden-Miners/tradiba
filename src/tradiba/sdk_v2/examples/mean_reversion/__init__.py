from tradiba.sdk_v2.strategy import Strategy
from tradiba.sdk_v2.subscriptions import on
from tradiba.sdk_v2.indicators import RSI
from tradiba.sdk_v2.parameters import IntParameter

class MeanReversionStrategy(Strategy):
    """
    RSI-based mean reversion.
    """
    rsi_window = IntParameter(default=14, minimum=2)
    overbought = IntParameter(default=70, maximum=99)
    oversold = IntParameter(default=30, minimum=1)
    
    def on_initialize(self, ctx):
        self.rsi = RSI(window=self.rsi_window) # type: ignore
        
    @on("candle")
    def on_candle(self, event):
        self.rsi.update(event["close"])
        
        # Look for mean reversion entries based on self.rsi.value()
