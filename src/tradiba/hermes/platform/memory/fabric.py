from typing import Any

class UnifiedMemoryFabric:
    """
    Exposes a single Memory SDK over working, episodic, semantic, long-term memory.
    """
    def __init__(self):
        self.store = {}
        
    def write(self, key: str, value: Any):
        self.store[key] = value
        
    def read(self, key: str) -> Any:
        return self.store.get(key)
