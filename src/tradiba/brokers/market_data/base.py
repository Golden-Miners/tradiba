from abc import ABC, abstractmethod
from typing import List, Any
from datetime import datetime

class MarketDataProvider(ABC):
    @abstractmethod
    def subscribe(self, symbols: List[str]) -> None:
        """Subscribe to real-time market data for the given symbols."""
        pass

    @abstractmethod
    def unsubscribe(self, symbols: List[str]) -> None:
        """Unsubscribe from real-time market data for the given symbols."""
        pass

    @abstractmethod
    def historical(self, symbol: str, start: datetime, end: datetime, timeframe: str) -> List[Any]:
        """Fetch historical data."""
        pass

    @abstractmethod
    def latest_quote(self, symbol: str) -> Any:
        """Get the most recent quote for a symbol."""
        pass
