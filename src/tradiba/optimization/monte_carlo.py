import random
from typing import List, Dict, Any


class MonteCarloEngine:
    """
    Shuffles trade outcomes to compute probabilistic metrics (e.g., Risk of Ruin).
    """

    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)

    def simulate(self, trade_results: List[float], iterations: int = 1000) -> Dict[str, Any]:
        """
        Runs `iterations` simulations of the trade sequence to calculate metrics.
        trade_results: list of PnL for each trade (e.g. [150.0, -50.0, 200.0, ...])
        """
        if not trade_results:
            return {}

        max_drawdowns = []
        final_equities = []

        for _ in range(iterations):
            # Shuffle the sequence of trades
            shuffled = trade_results.copy()
            self.rng.shuffle(shuffled)

            equity = 10000.0
            peak = equity
            max_dd = 0.0

            for pnl in shuffled:
                equity += pnl
                if equity > peak:
                    peak = equity
                dd = (peak - equity) / peak if peak > 0 else 0
                if dd > max_dd:
                    max_dd = dd

            max_drawdowns.append(max_dd)
            final_equities.append(equity)

        avg_dd = sum(max_drawdowns) / len(max_drawdowns)
        worst_dd = max(max_drawdowns)
        prob_of_ruin = sum(1 for e in final_equities if e <= 0) / len(final_equities)

        return {
            "iterations": iterations,
            "average_max_drawdown": avg_dd,
            "worst_case_drawdown": worst_dd,
            "probability_of_ruin": prob_of_ruin,
            "expected_final_equity": sum(final_equities) / len(final_equities)
        }
