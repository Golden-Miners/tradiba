from typing import Dict, Any, List
from datetime import datetime

class SharedMemory:
    """Maintains reusable context and historical analyses for agents."""
    
    def __init__(self):
        self._entries: List[Dict[str, Any]] = []
        
    def store(self, key: str, value: Any, agent_id: str):
        """Stores a versioned entry in memory."""
        self._entries.append({
            "key": key,
            "value": value,
            "agent_id": agent_id,
            "timestamp": datetime.utcnow().isoformat()
        })
        
    def retrieve(self, key: str) -> List[Dict[str, Any]]:
        """Retrieves all versions of a given key."""
        return [e for e in self._entries if e["key"] == key]
