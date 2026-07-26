from enum import Enum
from uuid import UUID

class Capability(Enum):
    PLUGINS = "plugins"
    AIOPS = "aiops"
    RESEARCH = "research"
    GPU = "gpu"
    DISTRIBUTED = "distributed"
    ANALYTICS = "analytics"

class LicenseManager:
    """Manages feature flags and capabilities per cluster."""
    def __init__(self) -> None:
        self._cluster_capabilities: dict[UUID, set[Capability]] = {}

    def grant_capability(self, cluster_id: UUID, capability: Capability) -> None:
        if cluster_id not in self._cluster_capabilities:
            self._cluster_capabilities[cluster_id] = set()
        self._cluster_capabilities[cluster_id].add(capability)

    def has_capability(self, cluster_id: UUID, capability: Capability) -> bool:
        return capability in self._cluster_capabilities.get(cluster_id, set())
