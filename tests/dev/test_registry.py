import pytest
from tradiba.dev.schemas import EventSchema
from tradiba.dev.registry import SchemaRegistry

def test_schema_registration():
    registry = SchemaRegistry()
    schema = EventSchema(name="test_event", version="1.0", fields={"price": float})
    
    registry.register(schema)
    assert registry.get("test_event") == schema
    
    with pytest.raises(ValueError):
        registry.register(schema)

def test_schema_validation():
    registry = SchemaRegistry()
    schema = EventSchema(name="trade", version="1.0", fields={"price": float, "qty": int})
    registry.register(schema)
    
    # Valid
    assert registry.validate_event("trade", {"price": 100.5, "qty": 10})
    
    # Invalid - missing field
    assert not registry.validate_event("trade", {"price": 100.5})
    
    # Invalid - wrong type
    assert not registry.validate_event("trade", {"price": "100.5", "qty": 10})
    
    # Invalid - unknown schema
    assert not registry.validate_event("unknown", {"price": 100.5})
