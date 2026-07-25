from tradiba.dev.schemas import EventSchema
from typing import Any

class SchemaRegistry:
    """
    Registry for event schemas to ensure serialization compatibility and versioning.
    """
    def __init__(self) -> None:
        self._schemas: dict[str, EventSchema] = {}

    def register(self, schema: EventSchema) -> None:
        if schema.name in self._schemas:
            raise ValueError(f"Schema {schema.name} is already registered.")
        self._schemas[schema.name] = schema

    def get(self, name: str) -> EventSchema | None:
        return self._schemas.get(name)

    def validate_event(self, name: str, data: dict[str, Any]) -> bool:
        schema = self.get(name)
        if not schema:
            return False
            
        for field, f_type in schema.fields.items():
            if field not in data:
                return False
            if not isinstance(data[field], f_type):
                return False
                
        return True

_global_registry = SchemaRegistry()

def register_schema(schema: EventSchema) -> None:
    _global_registry.register(schema)
    
def get_schema(name: str) -> EventSchema | None:
    return _global_registry.get(name)
