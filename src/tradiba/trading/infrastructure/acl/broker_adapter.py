class BrokerAdapter:
    """Anti-Corruption Layer translating external broker responses to internal domain concepts."""
    
    def translate_execution(self, broker_response: dict) -> dict:
        """
        Example: The broker calls it 'qty', we call it 'Quantity'.
        The broker calls it 'fill_px', we call it 'Price'.
        """
        return {
            "quantity": broker_response.get("qty"),
            "price": broker_response.get("fill_px")
        }
