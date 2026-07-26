from typing import Dict, List
from uuid import UUID
from tradiba.evolution.models.capability import Capability

class CapabilityRegistry:
    """Stores and retrieves registered capabilities."""
    
    def __init__(self) -> None:
        self._store: Dict[UUID, Capability] = {}
        
    def register(self, capability: Capability) -> None:
        self._store[capability.id] = capability
        
    def get(self, capability_id: UUID) -> Capability | None:
        return self._store.get(capability_id)
        
    def list_all(self) -> List[Capability]:
        return list(self._store.values())
