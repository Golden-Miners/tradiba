from typing import Protocol, Any, Dict

class ExecutionAlgorithm(Protocol):
    """Protocol for execution algorithms."""
    
    def on_tick(self, market_data: Any) -> None:
        """Called on every market data update."""
        ...
        
    def submit_order(self, order_details: Dict[str, Any]) -> str:
        """Initialize the execution of a parent order."""
        ...
        
    def cancel_order(self, order_id: str) -> bool:
        """Cancel the parent order and any working child orders."""
        ...

class IcebergAlgorithm:
    """
    Reference Implementation: Iceberg Execution Algorithm.
    Slices a large parent order into smaller visible child orders.
    """
    
    def __init__(self, broker_adapter: Any, display_size: float, variance_pct: float = 0.1):
        self.broker = broker_adapter
        self.display_size = display_size
        self.variance_pct = variance_pct
        self.active_orders: Dict[str, Dict[str, Any]] = {}
        
    def submit_order(self, order_details: Dict[str, Any]) -> str:
        """
        Submit a new parent iceberg order.
        order_details must contain: 'symbol', 'total_quantity', 'price', 'side'
        """
        parent_id = "ICEBERG-" + str(id(order_details))
        
        self.active_orders[parent_id] = {
            "symbol": order_details["symbol"],
            "total_quantity": order_details["total_quantity"],
            "remaining_quantity": order_details["total_quantity"],
            "price": order_details["price"],
            "side": order_details["side"],
            "current_child_id": None
        }
        
        self._slice_and_submit(parent_id)
        return parent_id
        
    def _slice_and_submit(self, parent_id: str):
        """Submit the next slice to the market."""
        order = self.active_orders.get(parent_id)
        if not order or order["remaining_quantity"] <= 0:
            return
            
        # Determine child size, optionally adding variance
        min(self.display_size, order["remaining_quantity"])
        
        # Mock broker submission
        child_id = f"CHILD-{parent_id}-{order['remaining_quantity']}"
        order["current_child_id"] = child_id
        
        # In a real system, we'd call self.broker.submit(...) here
        
    def on_child_fill(self, child_id: str, filled_qty: float):
        """Callback when a child order is filled."""
        for parent_id, order in self.active_orders.items():
            if order["current_child_id"] == child_id:
                order["remaining_quantity"] -= filled_qty
                order["current_child_id"] = None
                
                # Submit next slice if remaining
                if order["remaining_quantity"] > 0:
                    self._slice_and_submit(parent_id)
                break
