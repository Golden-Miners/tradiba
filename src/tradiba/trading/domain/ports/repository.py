from typing import Protocol, Any
import uuid

class OrderRepository(Protocol):
    """Port for order persistence."""
    
    def save(self, order: Any) -> None:
        """Save an order aggregate."""
        ...
        
    def load(self, order_id: uuid.UUID) -> Any:
        """Load an order aggregate."""
        ...
