from typing import Dict, Any

class WorkingMemory:
    """Stores the active task context for Hermes."""
    def __init__(self):
        self.context: Dict[str, Any] = {}

    def update(self, key: str, value: Any):
        self.context[key] = value

    def retrieve(self, key: str) -> Any:
        return self.context.get(key)
    
    def clear(self):
        self.context.clear()
