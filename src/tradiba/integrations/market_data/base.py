from abc import ABC, abstractmethod
from typing import Any, Dict, List
from datetime import datetime

class MarketDataAdapter(ABC):
    """
    Standard interface for market data providers.
    """

    @abstractmethod
    def subscribe_ticks(self, symbol: str, callback):
        """Subscribe to real-time tick data."""
        pass

    @abstractmethod
    def subscribe_bars(self, symbol: str, timeframe: str, callback):
        """Subscribe to real-time bar data."""
        pass

    @abstractmethod
    def get_historical_bars(self, symbol: str, timeframe: str, start: datetime, end: datetime) -> List[Dict[str, Any]]:
        """Fetch historical bars (candles)."""
        pass

    @abstractmethod
    def get_historical_ticks(self, symbol: str, start: datetime, end: datetime) -> List[Dict[str, Any]]:
        """Fetch historical ticks."""
        pass
