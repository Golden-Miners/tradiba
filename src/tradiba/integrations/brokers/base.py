from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BrokerAdapter(ABC):
    """
    Standard interface for all broker adapters.
    """

    @abstractmethod
    def connect(self) -> bool:
        """Connect to the broker."""
        pass

    @abstractmethod
    def disconnect(self) -> bool:
        """Disconnect from the broker."""
        pass

    @abstractmethod
    def submit_order(self, symbol: str, volume: float, order_type: str, price: Optional[float] = None) -> Dict[str, Any]:
        """Submit a new order."""
        pass

    @abstractmethod
    def cancel_order(self, ticket: int) -> bool:
        """Cancel an existing order."""
        pass

    @abstractmethod
    def modify_order(self, ticket: int, price: Optional[float] = None, sl: Optional[float] = None, tp: Optional[float] = None) -> bool:
        """Modify an existing order."""
        pass

    @abstractmethod
    def get_positions(self) -> List[Dict[str, Any]]:
        """Get all open positions."""
        pass

    @abstractmethod
    def get_orders(self) -> List[Dict[str, Any]]:
        """Get all pending orders."""
        pass

    @abstractmethod
    def get_account(self) -> Dict[str, Any]:
        """Get account summary (balance, equity, margin)."""
        pass

    @abstractmethod
    def stream_updates(self):
        """Stream account and order updates."""
        pass
