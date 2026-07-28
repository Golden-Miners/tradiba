from typing import Dict, Any, List

class CapabilityRegistry:
    """
    Capability advertising and lookup.
    """
    def __init__(self):
        self.capabilities: Dict[str, Dict[str, Any]] = {}

    def advertise(self, cap_name: str, metadata: Dict[str, Any]) -> None:
        self.capabilities[cap_name] = metadata

    def discover(self, capability: str) -> List[Dict[str, Any]]:
        if capability in self.capabilities:
            return [self.capabilities[capability]]
        return []
