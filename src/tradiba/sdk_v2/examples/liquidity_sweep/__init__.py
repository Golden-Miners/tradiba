from tradiba.sdk_v2.strategy import Strategy
from tradiba.sdk_v2.subscriptions import on

class LiquiditySweepStrategy(Strategy):
    """
    Looks for stops being run at major liquidity pools.
    """
    @on("candle")
    def on_candle(self, event):
        if not self.ctx:
            return
            
        sweeps = self.ctx.market.narrative.active_liquidity()
        
        # In a real strategy, this would look for sweeps followed by rejection
        return sweeps
