from typing import Dict, Any

class CognitiveCapabilityRegistry:
    """
    Registers capabilities with metadata.
    """
    def __init__(self):
        self.registry = {}
        
    def register(self, name: str, metadata: Dict[str, Any]):
        self.registry[name] = metadata
        
    def lookup(self, name: str) -> Dict[str, Any]:
        return self.registry.get(name, {})
