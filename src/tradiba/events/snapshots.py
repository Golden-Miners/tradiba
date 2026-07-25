from abc import ABC, abstractmethod
from typing import Any, Optional

class SnapshotStore(ABC):
    @abstractmethod
    def save(self, aggregate: Any) -> None:
        ...

    @abstractmethod
    def load(self, aggregate_id: str) -> Optional[Any]:
        ...
