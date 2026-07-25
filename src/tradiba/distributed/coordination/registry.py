# The actual storage implementation of the cluster registry (e.g. Postgres or Redis)
# To avoid a circular import with the cluster package, this might just be a backend interface.

from abc import ABC, abstractmethod
from typing import Dict, Any

class RegistryBackend(ABC):
    @abstractmethod
    def save_node(self, node_id: str, metadata: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def remove_node(self, node_id: str) -> None:
        pass

    @abstractmethod
    def get_all_nodes(self) -> Dict[str, dict[str, Any]]:
        pass
