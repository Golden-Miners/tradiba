from typing import Any

class Entity:
    """Base class for all Domain Entities."""
    def __init__(self, id: Any):
        self.id = id

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, type(self)):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)


class AggregateRoot(Entity):
    """Base class for Aggregate Roots."""
    def __init__(self, id: Any):
        super().__init__(id)
        self._domain_events: list[Any] = []

    def register_event(self, event: Any) -> None:
        self._domain_events.append(event)

    def clear_events(self) -> None:
        self._domain_events.clear()

    @property
    def domain_events(self) -> list[Any]:
        return list(self._domain_events)
