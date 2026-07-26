class TradingAPI:
    """Entrypoint for external systems to interact with the Trading domain."""
    
    def submit_order(self, payload: dict) -> dict:
        # In a real system, this would deserialize the payload,
        # instantiate the SubmitOrderHandler, and return a serialized Result.
        return {"status": "received"}
