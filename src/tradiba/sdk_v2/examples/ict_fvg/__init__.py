from tradiba.sdk_v2.strategy import Strategy
from tradiba.sdk_v2.subscriptions import on

class ICTFVGStrategy(Strategy):
    """
    ICT Fair Value Gap strategy utilizing the Market Narrative API.
    """
    @on("candle")
    def on_candle(self, event):
        if not self.ctx:
            return
            
        bias = self.ctx.market.narrative.bias()
        fvgs = self.ctx.market.narrative.active_fvgs()
        
        # In a real strategy, this would look for FVG retests aligned with bias
        return bias, fvgs
