from typing import Dict, Any

class OrderTicketService:
    """Handles pre-trade risk validation and order submission."""
    
    def validate_order(self, order_data: Dict[str, Any]) -> bool:
        # Mock risk validation: reject if position size > 10%
        if order_data.get("risk_percentage", 0) > 10.0:
            return False
        return True
        
    def submit_order(self, order_data: Dict[str, Any]) -> Dict[str, str]:
        if not self.validate_order(order_data):
            return {"status": "rejected", "reason": "risk_limit_exceeded"}
        return {"status": "submitted", "order_id": "ord_123"}
