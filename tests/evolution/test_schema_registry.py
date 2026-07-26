from tradiba.evolution.schema_registry import SchemaRegistry

def test_schema_registry():
    registry = SchemaRegistry()
    registry.register_schema("Trade", "v1", '{"fields": ["id", "price"]}')
    
    schema = registry.get_schema("Trade", "v1")
    assert schema is not None
    assert "price" in schema
