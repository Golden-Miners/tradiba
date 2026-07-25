from typing import List, Any
from datetime import datetime
from tradiba.brokers.market_data.base import MarketDataProvider

class MT5MarketDataProvider(MarketDataProvider):
    def subscribe(self, symbols: List[str]) -> None:
        pass

    def unsubscribe(self, symbols: List[str]) -> None:
        pass

    def historical(self, symbol: str, start: datetime, end: datetime, timeframe: str) -> List[Any]:
        return []

    def latest_quote(self, symbol: str) -> Any:
        return None
