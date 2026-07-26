
# This simulates a consumer-driven contract test
# E.g. "Risk" expects "Trading" to emit an OrderSubmitted event matching this schema

EXPECTED_ORDER_SUBMITTED_SCHEMA = {
    "type": "object",
    "properties": {
        "order_id": {"type": "string"},
        "symbol": {"type": "string"},
        "quantity": {"type": "number"},
        "price": {"type": "number"},
    },
    "required": ["order_id", "symbol", "quantity", "price"]
}

def test_order_submitted_contract():
    """Verify that the Trading domain's generated event matches the Risk domain's expectations."""
    # In a real scenario, this would load the actual event schema published by the provider
    actual_event_schema = {
        "type": "object",
        "properties": {
            "order_id": {"type": "string"},
            "symbol": {"type": "string"},
            "quantity": {"type": "number"},
            "price": {"type": "number"},
            "timestamp": {"type": "string"} # Extra fields are fine in JSON schema
        },
        "required": ["order_id", "symbol", "quantity", "price"]
    }
    
    # Check that all required fields from the consumer are present in the provider's schema
    for req in EXPECTED_ORDER_SUBMITTED_SCHEMA["required"]:
        assert req in actual_event_schema["properties"], f"Contract broken: Missing required field {req}"
        assert actual_event_schema["properties"][req]["type"] == EXPECTED_ORDER_SUBMITTED_SCHEMA["properties"][req]["type"]
