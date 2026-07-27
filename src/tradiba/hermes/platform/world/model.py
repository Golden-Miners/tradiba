from typing import Dict, Any

class UnifiedWorldModel:
    """
    Represents markets, portfolios, strategies, infra, orgs, AI systems, users, research.
    """
    def __init__(self):
        self.entities = {}
        
    def sync(self, entity_id: str, state: Dict[str, Any]):
        self.entities[entity_id] = state
        
    def get_state(self, entity_id: str) -> Dict[str, Any]:
        return self.entities.get(entity_id, {})
