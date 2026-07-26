from tradiba.evolution.models.capability import Capability, CapabilityStatus
import dataclasses
from typing import Dict
from uuid import UUID

class DeprecationLifecycle:
    """Manages the deprecation lifecycle for capabilities."""
    
    def __init__(self) -> None:
        self._notices: Dict[UUID, str] = {}
        
    def deprecate(self, capability: Capability, notice: str) -> Capability:
        self._notices[capability.id] = notice
        return dataclasses.replace(capability, status=CapabilityStatus.DEPRECATED)
        
    def remove(self, capability: Capability) -> Capability:
        return dataclasses.replace(capability, status=CapabilityStatus.REMOVED)
