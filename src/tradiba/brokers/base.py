from abc import ABC, abstractmethod
from typing import List, Dict, Any

from tradiba.brokers.models import Instrument, TradingAccount
from tradiba.brokers.capabilities import BrokerCapabilities
from tradiba.strategy.models import TradingSignal

class BrokerAdapter(ABC):
    @property
    @abstractmethod
    def capabilities(self) -> BrokerCapabilities:
        """Return the capabilities of this broker."""
        pass

    @abstractmethod
    def connect(self) -> None:
        """Connect to the broker API."""
        pass

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the broker API."""
        pass

    @abstractmethod
    def instruments(self) -> List[Instrument]:
        """Fetch available instruments."""
        pass

    @abstractmethod
    def account(self) -> TradingAccount:
        """Fetch account information."""
        pass

    @abstractmethod
    def positions(self) -> List[Any]:
        """Fetch current open positions."""
        pass

    @abstractmethod
    def submit(self, signal: TradingSignal) -> Any:
        """Submit an order."""
        pass

    @abstractmethod
    def modify(self, order_id: str, updates: Dict[str, Any]) -> Any:
        """Modify an existing order."""
        pass

    @abstractmethod
    def cancel(self, order_id: str) -> Any:
        """Cancel an order."""
        pass

    @abstractmethod
    def stream_ticks(self, symbols: List[str]) -> Any:
        """Subscribe to tick data streams."""
        pass
