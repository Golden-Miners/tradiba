from typing import Any, Dict, List, Optional
import uuid

from tradiba.integrations.brokers.base import BrokerAdapter

class PaperBrokerAdapter(BrokerAdapter):
    """
    A simulated broker for paper trading and sandbox environments.
    """
    def __init__(self):
        self._connected = False
        self._balance = 100000.0
        self._equity = 100000.0
        self._positions = {}
        self._orders = {}

    def connect(self) -> bool:
        self._connected = True
        return True

    def disconnect(self) -> bool:
        self._connected = False
        return True

    def submit_order(self, symbol: str, volume: float, order_type: str, price: Optional[float] = None) -> Dict[str, Any]:
        ticket = int(uuid.uuid4().int % 1000000)
        order = {
            "ticket": ticket,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "status": "ACCEPTED"
        }
        self._orders[ticket] = order
        return order

    def cancel_order(self, ticket: int) -> bool:
        if ticket in self._orders:
            self._orders[ticket]["status"] = "CANCELLED"
            return True
        return False

    def modify_order(self, ticket: int, price: Optional[float] = None, sl: Optional[float] = None, tp: Optional[float] = None) -> bool:
        if ticket in self._orders:
            if price: self._orders[ticket]["price"] = price
            return True
        return False

    def get_positions(self) -> List[Dict[str, Any]]:
        return list(self._positions.values())

    def get_orders(self) -> List[Dict[str, Any]]:
        return list(self._orders.values())

    def get_account(self) -> Dict[str, Any]:
        return {
            "balance": self._balance,
            "equity": self._equity,
            "margin": 0.0,
            "free_margin": self._equity
        }

    def stream_updates(self):
        pass
