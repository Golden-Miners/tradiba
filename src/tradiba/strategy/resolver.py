from collections import defaultdict
from .models import TradingSignal, SignalSide

class ConflictResolver:
    def __init__(self, margin: int = 20):
        self.margin = margin

    def resolve(self, signals: list[TradingSignal]) -> list[TradingSignal]:
        # Group by (symbol, timeframe)
        groups = defaultdict(list)
        for sig in signals:
            groups[(sig.symbol, sig.timeframe)].append(sig)

        resolved = []

        for (sym, tf), group_signals in groups.items():
            buy_score = sum(s.confidence for s in group_signals if s.side == SignalSide.BUY)
            sell_score = sum(s.confidence for s in group_signals if s.side == SignalSide.SELL)

            if buy_score > sell_score + self.margin:
                # BUY dominates
                resolved.extend(s for s in group_signals if s.side == SignalSide.BUY)
            elif sell_score > buy_score + self.margin:
                # SELL dominates
                resolved.extend(s for s in group_signals if s.side == SignalSide.SELL)
            else:
                # Conflict, no clear dominance. Emit no signal.
                pass

        return resolved
