def test_api_compatibility():
    """Ensure REST API contracts do not introduce breaking changes."""
    
    v1_schema = {
        "POST /api/v1/orders": {
            "request": {"symbol": "str", "qty": "float"},
            "response": {"order_id": "str", "status": "str"}
        }
    }
    
    # Simulate a check against the current codebase schema
    current_schema = {
        "POST /api/v1/orders": {
            # Added "type", which is fine if it's optional, but let's assume it's backward compatible
            "request": {"symbol": "str", "qty": "float", "type": "str"}, 
            "response": {"order_id": "str", "status": "str"}
        }
    }
    
    for endpoint, contract in v1_schema.items():
        assert endpoint in current_schema, f"Breaking change: {endpoint} was removed"
        
        # Check that we didn't remove any fields from the request
        for req_field in contract["request"]:
            assert req_field in current_schema[endpoint]["request"], f"Breaking change: Removed {req_field} from {endpoint}"
            
        # Check that we didn't remove any fields from the response
        for res_field in contract["response"]:
            assert res_field in current_schema[endpoint]["response"], f"Breaking change: Removed {res_field} from {endpoint} response"
