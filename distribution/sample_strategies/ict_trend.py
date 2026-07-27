from tradiba.strategy.interface import Strategy
from tradiba.strategy.models import TradingSignal, SignalType

class ICTTrendStrategy(Strategy):
    """
    Sample Strategy demonstrating Inner Circle Trader (ICT) concepts.
    Looks for Fair Value Gaps (FVG) and Market Structure Shifts (MSS) to ride trends.
    """
    def __init__(self, symbol: str, risk_percent: float = 1.0):
        self.symbol = symbol
        self.risk_percent = risk_percent

    def on_market_data(self, event):
        # Placeholder for strategy logic
        pass

    def on_fvg_detected(self, fvg_event):
        """Triggers when a Fair Value Gap is formed."""
        if fvg_event.is_bullish:
            # Generate buy signal
            signal = TradingSignal(
                symbol=self.symbol,
                type=SignalType.BUY,
                confidence=0.85,
                metadata={"reason": "Bullish FVG with MSS"}
            )
            self.emit_signal(signal)
