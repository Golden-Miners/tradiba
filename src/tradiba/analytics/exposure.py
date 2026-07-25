from tradiba.analytics.portfolio import PortfolioSnapshot
from collections import defaultdict

class ExposureAnalyzer:
    """
    Computes exposure breakdowns across multiple dimensions for a given portfolio snapshot.
    """
    def __init__(self, snapshot: PortfolioSnapshot):
        self.snapshot = snapshot

    def by_symbol(self) -> dict[str, float]:
        """Returns exposure keyed by instrument symbol."""
        exposures: dict[str, float] = defaultdict(float)
        for pos in self.snapshot.positions:
            # Stub assuming pos is dict-like for now
            sym = pos.get("symbol", "UNKNOWN")
            val = pos.get("notional_value", 0.0)
            exposures[sym] += float(val)
        return dict(exposures)

    def by_asset_class(self) -> dict[str, float]:
        """Returns exposure keyed by asset class."""
        exposures: dict[str, float] = defaultdict(float)
        for pos in self.snapshot.positions:
            cls = pos.get("asset_class", "UNKNOWN")
            val = pos.get("notional_value", 0.0)
            exposures[cls] += float(val)
        return dict(exposures)

    def by_currency(self) -> dict[str, float]:
        """Returns exposure keyed by currency."""
        exposures: dict[str, float] = defaultdict(float)
        for pos in self.snapshot.positions:
            ccy = pos.get("currency", "UNKNOWN")
            val = pos.get("notional_value", 0.0)
            exposures[ccy] += float(val)
        return dict(exposures)

    def by_strategy(self) -> dict[str, float]:
        """Returns exposure keyed by strategy."""
        exposures: dict[str, float] = defaultdict(float)
        for pos in self.snapshot.positions:
            strat = pos.get("strategy_id", "UNKNOWN")
            val = pos.get("notional_value", 0.0)
            exposures[strat] += float(val)
        return dict(exposures)

    def by_broker(self) -> dict[str, float]:
        """Returns exposure keyed by broker."""
        exposures: dict[str, float] = defaultdict(float)
        for pos in self.snapshot.positions:
            broker = pos.get("broker_id", "UNKNOWN")
            val = pos.get("notional_value", 0.0)
            exposures[broker] += float(val)
        return dict(exposures)
