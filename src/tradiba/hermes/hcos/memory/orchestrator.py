from typing import Dict, Any, List

class MemoryOrchestrator:
    """
    Provides a unified memory API to all cognitive components.
    Coordinates working, episodic, semantic, and long-term memory.
    """
    def __init__(self):
        self.working_memory: Dict[str, Any] = {}
        self.episodic_memory: List[Dict[str, Any]] = []
        
    def write_working_memory(self, key: str, value: Any):
        self.working_memory[key] = value
        
    def read_working_memory(self, key: str) -> Any:
        return self.working_memory.get(key)
        
    def store_episode(self, episode: Dict[str, Any]):
        self.episodic_memory.append(episode)
        
    def retrieve_episodes(self, query: str) -> List[Dict[str, Any]]:
        # In a real system, this would use vector retrieval
        return [ep for ep in self.episodic_memory if query in str(ep)]
