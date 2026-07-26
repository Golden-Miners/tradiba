from typing import Dict

class SchemaRegistry:
    """Manages versioned schemas for domain models and events."""
    
    def __init__(self) -> None:
        self._schemas: Dict[str, Dict[str, str]] = {}
        
    def register_schema(self, schema_name: str, version: str, definition: str) -> None:
        if schema_name not in self._schemas:
            self._schemas[schema_name] = {}
        self._schemas[schema_name][version] = definition
        
    def get_schema(self, schema_name: str, version: str) -> str | None:
        return self._schemas.get(schema_name, {}).get(version)
