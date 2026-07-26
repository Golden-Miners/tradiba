from tradiba.trading.domain.ports.repository import OrderRepository
from tradiba.shared.contracts.result import Result
import uuid

class SubmitOrderHandler:
    """Application service for submitting orders."""
    
    def __init__(self, repository: OrderRepository):
        self.repository = repository
        
    def handle(self, order_data: dict) -> Result[uuid.UUID, str]:
        # Application layer orchestrates: validation, fetching, saving
        # Business rules are in the domain entities.
        
        # Example validation
        if "amount" not in order_data:
            return Result.fail("Missing amount")
            
        return Result.ok(uuid.uuid4())
